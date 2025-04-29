# admin_functions.py


import matplotlib.pyplot as plt
import mysql.connector
import database
from database import create_connection


def admin_view_student_details(student_id):
    enrolled_courses = database.get_enrolled_courses(student_id)
    grades = database.get_student_grades(student_id)
    progress = database.track_progress(student_id)
    report = database.generate_report(student_id)

    # Add number of modules per enrolled course
    course_details = []
    for course in enrolled_courses:
        course_id = course[0]
        course_name = course[1]
        module_count = database.get_module_count_for_course(course_id)
        course_details.append({
            "course_id": course_id,
            "course_name": course_name,
            "module_count": module_count
        })

    student_info = {
        "courses": course_details,
        "grades": grades,
        "progress": progress,
        "report": report
    }

    # --- Print nicely ---
    print("\n--- Student Details ---")
    if course_details:
        print("Enrolled Courses:")
        for course in course_details:
            print(f"Course ID: {course['course_id']}, Name: {course['course_name']}, Modules: {course['module_count']}")
    else:
        print("No enrolled courses.")

    if grades:
        print("\nGrades:")
        for grade in grades:
            print(f"Course ID: {grade[0]}, Grade: {grade[1]}")
    else:
        print("\nNo grades available.")

    if progress is not None:
        print("\nProgress:")
        print(f"Average Progress: {progress}%")
    else:
        print("\nNo progress data.")

    if report:
        print("\nGenerated Report:")
        print(report)
    else:
        print("\nNo report available.")

    return student_info


def view_progress_graph(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch courses and grades for the student
    query = """
    SELECT c.course_name, g.grade
    FROM courses c
    JOIN grades g ON c.course_id = g.course_id
    WHERE g.student_id = %s
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    if not data:
        print("No progress data found.")
        return

    courses = [course for course, grade in data]
    grades = [grade for course, grade in data]

    plt.bar(courses, grades, color='skyblue')
    plt.xlabel('Courses')
    plt.ylabel('Grades')
    plt.title('Your Progress in Each Course')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    conn.close()


def view_pass_fail_pie_chart():
    # Connect to the database
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query to count pass and fail students
    query = """
    SELECT 
        SUM(CASE WHEN grade >= 50 THEN 1 ELSE 0 END) AS passed,
        SUM(CASE WHEN grade < 50 THEN 1 ELSE 0 END) AS failed
    FROM grades
    """
    cursor.execute(query)
    result = cursor.fetchone()
    
    # Close the connection
    cursor.close()
    connection.close()

    # Prepare data for pie chart
    passed = result[0]
    failed = result[1]

    # Plot the pie chart
    labels = ['Passed', 'Failed']
    sizes = [passed, failed]
    colors = ['#4CAF50', '#FF5722']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Pass/Fail Distribution of Students')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()