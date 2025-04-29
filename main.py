import tkinter as tk
from tkinter import messagebox
import database
import admin
import student 
from tkinter import ttk
import time


# Colors
BG_LIGHT_BLUE = "#e6f2ff"
BG_DARK_BLUE = "#003366"
WHITE = "#ffffff"


# Centering window function
def center_window(window, width=600, height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Main App Class
class OnlineCourseAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Course Analyzer")
        self.root.configure(bg=BG_LIGHT_BLUE)
        center_window(self.root)

        self.frame = tk.Frame(root, bg=WHITE, padx=20, pady=20)
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Online Course Analyzer", font=("Helvetica", 24, "bold"), bg=WHITE, fg=BG_DARK_BLUE)
        self.title_label.pack(pady=(0, 20))

        self.login_button = tk.Button(self.frame, text="Login", command=self.login, bg=BG_DARK_BLUE, fg=WHITE, font=("Helvetica", 14), width=20)
        self.login_button.pack(pady=10)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.signup, bg=BG_DARK_BLUE, fg=WHITE, font=("Helvetica", 14), width=20)
        self.signup_button.pack(pady=10)

        self.exit_button = tk.Button(self.frame, text="Exit", command=self.root.quit, bg="red", fg=WHITE, font=("Helvetica", 14), width=20)
        self.exit_button.pack(pady=10)



    def login(self):
        show_loading("Loading...")  # Show spinner before fetching
        username = simple_input("Username")
        password = simple_input("Password", show='*')
        user = database.authenticate_user(username, password)

        if user:
            messagebox.showinfo("Success", f"Login successful! Welcome {user[1]}")
            if user[2] == 'admin':
                self.admin_dashboard()
            else:
                self.student_dashboard(user[0])
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again")



    def signup(self):
        username = simple_input("New Username")
        password = simple_input("New Password", show='*')
        email = simple_input("Email")
        role = simple_input("Role (admin/student)").lower()
        show_loading("Signing up...")  # Show spinner before fetching

        if role not in ['admin', 'student']:
            messagebox.showerror("Error", "Invalid role. Must be 'admin' or 'student'.")
            return

        connection = database.create_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists.")
        else:
            database.add_user(username, password, role, email)
            messagebox.showinfo("Success", "Sign up successful! Please login.")

        cursor.close()
        connection.close()


    def logout(self, dashboard_window):
        dashboard_window.destroy()  # Close the current dashboard window
        self.__init__(self.root)     



    def admin_dashboard(self):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Admin Dashboard")
        dashboard_window.configure(bg=BG_LIGHT_BLUE)
        center_window(dashboard_window)

        dashboard_frame = tk.Frame(dashboard_window, bg=WHITE, padx=20, pady=20)
        dashboard_frame.pack(expand=True)

        # Add the Logout button for admin
        logout_button = tk.Button(dashboard_frame, text="Logout", command=lambda: self.logout(dashboard_window), bg="red", fg=WHITE, font=("Helvetica", 14), width=20)
        logout_button.pack(pady=10)

        options = [
            ("View All Courses", lambda: display_data(database.get_all_courses(), 
                                              column_names=["Course ID", "Course Name", "Instructor"])),
            ("Add Course", self.add_course),
            ("Add Module", self.add_module),
            ("Enroll Student", self.enroll_student),
            ("View Student Progress", self.view_progress),
            ("Generate Student Report", self.generate_report),
            ("Update Grade", self.update_grade),
            ("View Student Details", self.view_student_details),
            ("View Modules by Course",self.view_modules_by_course)
        ]

        for text, command in options:
            btn = tk.Button(dashboard_frame, text=text, command=command, bg=BG_DARK_BLUE, fg=WHITE, font=("Helvetica", 12), width=30)
            btn.pack(pady=5)


    def student_dashboard(self, student_id):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Student Dashboard")
        dashboard_window.configure(bg=BG_LIGHT_BLUE)
        center_window(dashboard_window)

        dashboard_frame = tk.Frame(dashboard_window, bg=WHITE, padx=20, pady=20)
        dashboard_frame.pack(expand=True)

         # Add the Logout button for student
        logout_button = tk.Button(dashboard_frame, text="Logout", command=lambda: self.logout(dashboard_window), bg="red", fg=WHITE, font=("Helvetica", 14), width=20)
        logout_button.pack(pady=10)

        options = [
            ("View Enrolled Courses", lambda: display_data(database.get_enrolled_courses(student_id),column_names=["Course ID", "Course Name"])),
            ("View Grades", lambda: display_data(database.get_student_grades(student_id),column_names=[ "Course Name", "Module Name", "Grade"])),
            ("Track Progress", lambda: student.view_progress_graph(student_id)),
            ("Access Report", lambda: student.generate_student_report(student_id))
        ]

        for text, command in options:
            btn = tk.Button(dashboard_frame, text=text, command=command, bg=BG_DARK_BLUE, fg=WHITE, font=("Helvetica", 12), width=30)
            btn.pack(pady=5)


    def add_course(self):
        course_name = simple_input("Course Name")
        instructor_id = simple_input("Instructor ID")
        
        # Call the database's add_course function
        result = database.add_course(course_name, instructor_id)
        
        if result:  # If result is True (course added successfully)
            messagebox.showinfo("Success", "Course added!")
        else:  # If result is False (error occurred)
            messagebox.showerror("Error", "Instructor must be an admin. Try again!")


    def add_module(self):
        course_id = simple_input("Course ID")
        module_name = simple_input("Module Name")
        description = simple_input("Module Description")
        
        # Call the add_module function in database.py
        result = database.add_module(course_id, module_name, description)
        
        if result:  # If result is True (module added successfully)
            messagebox.showinfo("Success", "Module added!")
        else:  # If result is False (course does not exist)
            messagebox.showerror("Error", "Course does not exist. Please check the Course ID.")



    def enroll_student(self):
        student_id = simple_input("Student ID")
        course_id = simple_input("Course ID")
        
        # Call the enroll_student function in database.py and capture the result
        result = database.enroll_student(student_id, course_id)
        
        if result:  # If enrollment was successful
            messagebox.showinfo("Success", "Student enrolled!")
        else:  # If enrollment failed (either student is not a student or course does not exist)
            messagebox.showerror("Error", "Enrollment failed. Please ensure student ID is correct and course ID exists.")
 

    def view_progress(self):
        student_id = simple_input("Student ID")
        show_loading("Fetching...")  # Show spinner before fetching
        error_message = student.view_progress_graph(student_id)  # Get the error message from the function

        if error_message:  # If an error message is returned
            messagebox.showerror("Error", error_message)  # Show error message in UI


    def generate_report(self):
        student_id = simple_input("Student ID")
        show_loading("Fetching...")  # Show spinner before fetching
        student.generate_student_report(student_id)
        #display_data(report)

    def update_grade(self):
        student_id = simple_input("Student ID")
        module_id = simple_input("Module ID")
        grade = simple_input("Grade")
        database.update_grade(student_id, module_id, grade)
        #Smessagebox.showinfo("Success", "Grade updated!")

    def view_student_details(self):
        student_id = simple_input("Student ID")
        details = admin.admin_view_student_details(student_id)
        display_student_report(details)

    def view_modules_by_course(self):
        # Ask the user for Course ID
        course_id = simple_input("Course ID")

        if course_id:
            modules = database.get_modules_by_course(course_id)
            if modules:
                display_data(modules, column_names=["Module ID", "Course ID", "Module Name", "Content"])
            else:
                messagebox.showinfo("Info", "No modules found for this Course ID.")
        else:
            messagebox.showwarning("Warning", "No Course ID entered.")



# Helper Functions
def simple_input(title, show=None):
    input_window = tk.Toplevel()
    input_window.title(title)
    center_window(input_window, 300, 150)
    input_window.configure(bg=BG_LIGHT_BLUE)

    tk.Label(input_window, text=title, bg=BG_LIGHT_BLUE, font=("Helvetica", 12)).pack(pady=10)
    entry = tk.Entry(input_window, show=show)
    entry.pack(pady=5)
    result = []

    def submit():
        result.append(entry.get())
        input_window.destroy()

    submit_btn = tk.Button(input_window, text="Submit", command=submit, bg=BG_DARK_BLUE, fg=WHITE)
    submit_btn.pack(pady=10)

    input_window.grab_set()
    input_window.wait_window()
    return result[0] if result else None


def display_data(data, column_names=None):
    output_window = tk.Toplevel()
    output_window.title("Data")
    center_window(output_window, 800, 400)
    output_window.configure(bg=BG_LIGHT_BLUE)

    if not data:
        tk.Label(output_window, text="No data found.", bg=BG_LIGHT_BLUE, font=("Helvetica", 14)).pack(pady=20)
        return

    tree = ttk.Treeview(output_window)
    tree.pack(expand=True, fill="both")

    # Set columns
    if isinstance(data, list):
        if not column_names:
            # Default names if not provided
            column_names = [f"Column {i+1}" for i in range(len(data[0]))]

        tree["columns"] = column_names
        tree["show"] = "headings"

        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for row in data:
            tree.insert("", "end", values=row)
    else:
        tree["columns"] = ("Data",)
        tree.heading("Data", text="Data")
        tree.column("Data", anchor="center")
        tree.insert("", "end", values=(str(data),))


def display_student_report(student_details):
    output_window = tk.Toplevel()
    output_window.title("Student Report")
    center_window(output_window, 800, 400)
    output_window.configure(bg=BG_LIGHT_BLUE)

    if not student_details:
        tk.Label(output_window, text="No data found.", bg=BG_LIGHT_BLUE, font=("Helvetica", 14)).pack(pady=20)
        return

    report_frame = tk.Frame(output_window, bg=BG_LIGHT_BLUE)
    report_frame.pack(expand=True)

    # Display Enrolled Courses
    enrolled_courses_label = tk.Label(report_frame, text="Enrolled Courses:", font=("Helvetica", 16, "bold"), bg=BG_LIGHT_BLUE)
    enrolled_courses_label.pack(anchor="w", padx=10, pady=5)

    for course in student_details.get("courses", []):
        course_text = f"Course ID: {course['course_id']}, Name: {course['course_name']}, Modules: {course['module_count']}"
        course_label = tk.Label(report_frame, text=course_text, font=("Helvetica", 12), bg=BG_LIGHT_BLUE)
        course_label.pack(anchor="w", padx=10)

    # Display Grades
    grades_label = tk.Label(report_frame, text="Grades:", font=("Helvetica", 16, "bold"), bg=BG_LIGHT_BLUE)
    grades_label.pack(anchor="w", padx=10, pady=5)

    for grade in student_details.get("grades", []):
        grade_text = f"Course ID: {grade[0]}, Grade: {grade[1]}"
        grade_label = tk.Label(report_frame, text=grade_text, font=("Helvetica", 12), bg=BG_LIGHT_BLUE)
        grade_label.pack(anchor="w", padx=10)

    # Display Progress
    progress_label = tk.Label(report_frame, text="Progress:", font=("Helvetica", 16, "bold"), bg=BG_LIGHT_BLUE)
    progress_label.pack(anchor="w", padx=10, pady=5)

    progress_text = f"Average Progress: {student_details.get('progress', 0)}%"
    progress_label = tk.Label(report_frame, text=progress_text, font=("Helvetica", 12), bg=BG_LIGHT_BLUE)
    progress_label.pack(anchor="w", padx=10)

    # Display Generated Report
    report_label = tk.Label(report_frame, text="Generated Report:", font=("Helvetica", 16, "bold"), bg=BG_LIGHT_BLUE)
    report_label.pack(anchor="w", padx=10, pady=5)

    for report in student_details.get("report", []):
        report_text = f"Course ID: {report[0]}, Module: {report[1]}, Grade: {report[2]}"
        report_label = tk.Label(report_frame, text=report_text, font=("Helvetica", 12), bg=BG_LIGHT_BLUE)
        report_label.pack(anchor="w", padx=10)


def display_message(message):
    messagebox.showinfo("Info", message)
    

# Theme setting
def toggle_theme():
    if style.theme_use() == "default":
        style.theme_use("clam")  # or 'alt', 'clam', 'vista', 'xpnative'
        root.configure(bg="black")
    else:
        style.theme_use("default")
        root.configure(bg="white")

root = tk.Tk()
root.title("Online Course Analyzer System")
style = ttk.Style(root)

# Add a Theme Toggle Button
theme_btn = tk.Button(root, text="Toggle Theme 🌗", command=toggle_theme)
theme_btn.pack(pady=5)

root.attributes('-alpha', 0.0)  # Start fully transparent

def fade_in():
    alpha = 0.0
    while alpha < 1.0:
        alpha += 0.01
        root.attributes('-alpha', alpha)
        root.update()
        time.sleep(0.01)

fade_in()

# Function to show loading spinner message
def show_loading(message="Loading..."):
    loading_label = tk.Label(root, text=message, font=("Arial", 14), fg=BG_DARK_BLUE, bg=BG_LIGHT_BLUE)
    loading_label.pack(pady=20)
    root.update()
    time.sleep(1)  # Simulate loading time (you can adjust the sleep time)
    loading_label.destroy()
    
    
# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineCourseAnalyzerApp(root)
    root.mainloop()
