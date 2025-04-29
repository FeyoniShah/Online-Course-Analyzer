

import database
import matplotlib.pyplot as plt
import mysql.connector
from database import create_connection
from fpdf import FPDF


def view_progress_graph(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Updated query to ensure all courses the student is enrolled in are included, even without grades
    query = """
    SELECT 
        courses.course_name, 
        modules.module_name, 
        COALESCE(grades.grade, 0) AS grade
    FROM 
        enrollments
    JOIN 
        courses ON enrollments.course_id = courses.course_id
    LEFT JOIN 
        modules ON courses.course_id = modules.course_id
    LEFT JOIN 
        grades ON grades.module_id = modules.module_id AND grades.student_id = %s
    WHERE 
        enrollments.student_id = %s
    """
    cursor.execute(query, (user_id, user_id))
    data = cursor.fetchall()

    if not data:
        return "No progress data found"  # Return the error message

    # Fix the issue with unpacking the data
    courses = [row[0] for row in data]  # Access the course_name (first column)
    grades = [row[2] for row in data]   # Access the grade (third column)

    # Plotting the data
    plt.bar(courses, grades, color='skyblue')
    plt.xlabel('Courses')
    plt.ylabel('Grades')
    plt.title('Your Progress in Each Course')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    conn.close()
    return None



def generate_student_report(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch student details
    cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    username, email = user

    # Fetch courses and grades
    cursor.execute("""
        SELECT c.course_name, g.grade
        FROM courses c
        JOIN modules m ON m.course_id = c.course_id
        JOIN grades g ON g.module_id = m.module_id
        WHERE g.student_id = %s
    """, (user_id,))

    data = cursor.fetchall()

    if not data:
        print("No data to generate report.")
        return

    # Generate Progress Graph
    courses = [course for course, grade in data]
    grades = [grade for course, grade in data]

    plt.bar(courses, grades, color='lightgreen')
    plt.xlabel('Courses')
    plt.ylabel('Grades')
    plt.title('Progress in Each Course')
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph_filename = "progress_graph.png"
    plt.savefig(graph_filename)
    plt.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Student Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Name: {username}", ln=True)
    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.cell(0, 10, f"Student ID: {user_id}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Courses and Grades", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", '', 12)
    for course, grade in data:
        pdf.cell(0, 10, f"{course}: {grade}", ln=True)

    pdf.ln(10)
    pdf.image(graph_filename, x=10, y=None, w=180)

    report_filename = f"student_report_{user_id}.pdf"
    pdf.output(report_filename)
    print(f"Report generated successfully: {report_filename}")

    conn.close()