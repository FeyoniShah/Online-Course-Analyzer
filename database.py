import mysql.connector

def create_connection():
    try:
        
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Feyoni@1819",
            database="online_course_analyzer" 
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None



# Function to add a new user (Admin or Student)
def add_user(username, password, role, email):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password, role, email, registration_date, status) VALUES (%s, %s, %s, %s, NOW(), 'active')"
    cursor.execute(query, (username, password, role, email))
    connection.commit()
    cursor.close()
    connection.close()

# Function to authenticate a user (Admin or Student)
def authenticate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

# Function to add a new course
'''def add_course(course_name, instructor_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO courses (course_name, instructor_id) VALUES (%s, %s)"
    cursor.execute(query, (course_name, instructor_id))
    connection.commit()
    cursor.close()
    connection.close()'''

def add_course(course_name, instructor_id):
    connection = create_connection()
    cursor = connection.cursor()

    # First, check if the instructor_id belongs to an admin
    check_query = "SELECT role FROM users WHERE id = %s"
    cursor.execute(check_query, (instructor_id,))
    result = cursor.fetchone()

    if result and result[0] == 'admin':  # Assuming 'role' column stores 'admin' or 'student'
        # If the user is an admin, insert the course
        insert_query = "INSERT INTO courses (course_name, instructor_id) VALUES (%s, %s)"
        cursor.execute(insert_query, (course_name, instructor_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True  # Return True if the course is added successfully
    else:
        cursor.close()
        connection.close()
        return False  # Return False if the instructor is not an admin



# Function to get all courses
def get_all_courses():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM courses"
    cursor.execute(query)
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return courses

# Function to add a new module for a course
def add_module(course_id, module_name, description):
    connection = create_connection()
    cursor = connection.cursor()

    # First, check if the course_id exists
    check_query = "SELECT COUNT(*) FROM courses WHERE course_id = %s"
    cursor.execute(check_query, (course_id,))
    result = cursor.fetchone()

    if result[0] > 0:  # If the course exists
        # Insert the module into the database
        insert_query = "INSERT INTO modules (course_id, module_name, description) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (course_id, module_name, description))
        connection.commit()
        cursor.close()
        connection.close()
        return True  # Return True if the module is added successfully
    else:
        cursor.close()
        connection.close()
        return False  # Return False if the course does not exist


# Function to enroll a student in a course
'''def enroll_student(student_id, course_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)"
    cursor.execute(query, (student_id, course_id))
    connection.commit()
    cursor.close()
    connection.close()'''

'''def enroll_student(student_id, course_id):
    connection = create_connection()
    cursor = connection.cursor()

    # First, check if the ID belongs to a student
    check_query = "SELECT role FROM users WHERE id = %s"  # use correct column name
    cursor.execute(check_query, (student_id,))
    result = cursor.fetchone()

    if result and result[0] == 'student':  # assuming 'student' is stored as role
        # Proceed to enroll
        enroll_query = "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)"
        cursor.execute(enroll_query, (student_id, course_id))
        connection.commit()
        print("Student enrolled successfully.")
    else:
        print("Error: Only students can be enrolled.")

    cursor.close()
    connection.close()
'''

def enroll_student(student_id, course_id):
    connection = create_connection()
    cursor = connection.cursor()

    # First, check if the student_id belongs to a student
    check_student_query = "SELECT role FROM users WHERE id = %s"
    cursor.execute(check_student_query, (student_id,))
    student_result = cursor.fetchone()

    if student_result and student_result[0] == 'student':  # Check if student exists
        # Now, check if the course_id exists
        check_course_query = "SELECT COUNT(*) FROM courses WHERE course_id = %s"
        cursor.execute(check_course_query, (course_id,))
        course_result = cursor.fetchone()

        if course_result[0] > 0:  # If the course exists
            # Proceed with enrollment
            enroll_query = "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)"
            cursor.execute(enroll_query, (student_id, course_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True  # Enrollment successful
        else:
            cursor.close()
            connection.close()
            return False  # Course does not exist
    else:
        cursor.close()
        connection.close()
        return False  # Student does not exist or is not a student



# Function to get enrolled courses for a student
'''
def get_enrolled_courses(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT courses.course_name FROM courses JOIN enrollments ON courses.course_id = enrollments.course_id WHERE enrollments.student_id = %s"
    cursor.execute(query, (student_id,))
    enrolled_courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return enrolled_courses

'''

def get_enrolled_courses(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
        SELECT c.course_id, c.course_name
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.student_id = %s
    """
    cursor.execute(query, (student_id,))
    enrolled_courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return enrolled_courses


# Function to update grades for a student in a module
'''
def update_grade(student_id, module_id, grade):
    connection = create_connection()
    cursor = connection.cursor()
    
    # Check if the student already has a grade entry for the given module
    query_check = "SELECT COUNT(*) FROM grades WHERE student_id = %s AND module_id = %s"
    cursor.execute(query_check, (student_id, module_id))
    result = cursor.fetchone()
    
    if result[0] > 0:  # If record exists, update the grade
        query_update = "UPDATE grades SET grade = %s WHERE student_id = %s AND module_id = %s"
        cursor.execute(query_update, (grade, student_id, module_id))
        print(f"Grade updated for student {student_id} in module {module_id}.")
    else:  # If no record exists, insert a new grade
        query_insert = "INSERT INTO grades (student_id, module_id, grade) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (student_id, module_id, grade))
        print(f"New grade inserted for student {student_id} in module {module_id}.")
    
    connection.commit()
    cursor.close()
    connection.close()'''

'''def update_grade(student_id, module_id, grade):
    connection = create_connection()
    cursor = connection.cursor()
    
    # Ask if the grade should be finalized
    finalize = input(f"Do you want to finalize the grade {grade} for student {student_id} in module {module_id}? (yes/no): ")
    is_final = 1 if finalize.lower() == 'yes' else 0

    # Check if the student already has a grade entry for the given module
    query_check = "SELECT COUNT(*) FROM grades WHERE student_id = %s AND module_id = %s"
    cursor.execute(query_check, (student_id, module_id))
    result = cursor.fetchone()
    
    if result[0] > 0:
        query_update = "UPDATE grades SET grade = %s, is_final = %s WHERE student_id = %s AND module_id = %s"
        cursor.execute(query_update, (grade, is_final, student_id, module_id))
        print(f"Grade updated for student {student_id} in module {module_id}.")
    else:
        query_insert = "INSERT INTO grades (student_id, module_id, grade, is_final) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_insert, (student_id, module_id, grade, is_final))
        print(f"New grade inserted for student {student_id} in module {module_id}.")

    connection.commit()
    cursor.close()
    connection.close()
'''


'''def update_grade(student_id, module_id, grade):
    connection = create_connection()
    cursor = connection.cursor()
    
    # Check if the student is enrolled in the course corresponding to the module
    query_check_enrollment = """
    SELECT COUNT(*) 
    FROM enrollments e
    JOIN modules m ON e.course_id = m.course_id
    WHERE e.student_id = %s AND m.module_id = %s AND e.enrollment_status = 'enrolled'
    """
    cursor.execute(query_check_enrollment, (student_id, module_id))
    result_enrollment = cursor.fetchone()
    
    if result_enrollment[0] == 0:
        print(f"Student {student_id} is not enrolled in the course containing module {module_id}. Grade update is not allowed.")
        cursor.close()
        connection.close()
        return
    
    # Ask if the grade should be finalized
    finalize = input(f"Do you want to finalize the grade {grade} for student {student_id} in module {module_id}? (yes/no): ")
    is_final = 1 if finalize.lower() == 'yes' else 0

    # Check if the student already has a grade entry for the given module
    query_check = "SELECT COUNT(*) FROM grades WHERE student_id = %s AND module_id = %s"
    cursor.execute(query_check, (student_id, module_id))
    result = cursor.fetchone()
    
    if result[0] > 0:
        query_update = "UPDATE grades SET grade = %s, is_final = %s WHERE student_id = %s AND module_id = %s"
        cursor.execute(query_update, (grade, is_final, student_id, module_id))
        print(f"Grade updated for student {student_id} in module {module_id}.")
    else:
        query_insert = "INSERT INTO grades (student_id, module_id, grade, is_final) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_insert, (student_id, module_id, grade, is_final))
        print(f"New grade inserted for student {student_id} in module {module_id}.")

    connection.commit()
    cursor.close()
    connection.close()'''


from tkinter import messagebox

def update_grade(student_id, module_id, grade):
    connection = create_connection()
    cursor = connection.cursor()

    # Check if the student exists
    query_check_student = "SELECT COUNT(*) FROM users WHERE id = %s AND role = 'student'"
    cursor.execute(query_check_student, (student_id,))
    result_student = cursor.fetchone()
    
    if result_student[0] == 0:
        messagebox.showerror("Error", f"Student with ID {student_id} does not exist or is not a valid student.")
        cursor.close()
        connection.close()
        return

    # Check if the module exists
    query_check_module = "SELECT COUNT(*) FROM modules WHERE module_id = %s"
    cursor.execute(query_check_module, (module_id,))
    result_module = cursor.fetchone()
    
    if result_module[0] == 0:
        messagebox.showerror("Error", f"Module with ID {module_id} does not exist.")
        cursor.close()
        connection.close()
        return

    # Check if the student is enrolled in the course corresponding to the module
    query_check_enrollment = """
    SELECT COUNT(*) 
    FROM enrollments e
    JOIN modules m ON e.course_id = m.course_id
    WHERE e.student_id = %s AND m.module_id = %s AND e.enrollment_status = 'enrolled'
    """
    cursor.execute(query_check_enrollment, (student_id, module_id))
    result_enrollment = cursor.fetchone()

    if result_enrollment[0] == 0:
        messagebox.showerror("Error", f"Student {student_id} is not enrolled in the course containing module {module_id}. Grade update is not allowed.")
        cursor.close()
        connection.close()
        return
    
    # Ask if the grade should be finalized
    finalize = messagebox.askquestion("Finalize Grade", f"Do you want to finalize the grade {grade} for student {student_id} in module {module_id}?")

    is_final = 1 if finalize == 'yes' else 0

    # Check if the student already has a grade entry for the given module
    query_check = "SELECT COUNT(*) FROM grades WHERE student_id = %s AND module_id = %s"
    cursor.execute(query_check, (student_id, module_id))
    result = cursor.fetchone()

    if result[0] > 0:
        query_update = "UPDATE grades SET grade = %s, is_final = %s WHERE student_id = %s AND module_id = %s"
        cursor.execute(query_update, (grade, is_final, student_id, module_id))
        messagebox.showinfo("Success", f"Grade updated for student {student_id} in module {module_id}.")
    else:
        query_insert = "INSERT INTO grades (student_id, module_id, grade, is_final) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_insert, (student_id, module_id, grade, is_final))
        messagebox.showinfo("Success", f"New grade inserted for student {student_id} in module {module_id}.")

    connection.commit()
    cursor.close()
    connection.close()



# Function to get grades for a student
'''def get_student_grades(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT modules.module_name, grades.grade FROM grades JOIN modules ON grades.module_id = modules.module_id WHERE grades.student_id = %s"
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()
    cursor.close()
    connection.close()
    return grades'''

def get_student_grades(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
        SELECT courses.course_name, modules.module_name, grades.grade
        FROM grades
        JOIN modules ON grades.module_id = modules.module_id
        JOIN courses ON modules.course_id = courses.course_id
        WHERE grades.student_id = %s
    """
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()
    cursor.close()
    connection.close()
    return grades


# Function to generate performance report for a student
def generate_report(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT courses.course_name, modules.module_name, grades.grade
    FROM grades
    JOIN modules ON grades.module_id = modules.module_id
    JOIN courses ON modules.course_id = courses.course_id
    WHERE grades.student_id = %s
    """
    cursor.execute(query, (student_id,))
    report = cursor.fetchall()
    cursor.close()
    connection.close()
    return report

# Function to track progress (average grade across all modules)
def track_progress(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT AVG(grades.grade) FROM grades
    WHERE grades.student_id = %s
    """
    cursor.execute(query, (student_id,))
    avg_grade = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return avg_grade


def get_module_count_for_course(course_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM modules WHERE course_id = %s"
    cursor.execute(query, (course_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count


def get_modules_by_course(course_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT module_id,course_id, module_name, description  FROM modules WHERE course_id = %s"
    cursor.execute(query, (course_id,))
    modules = cursor.fetchall()
    cursor.close()
    connection.close()
    return modules
