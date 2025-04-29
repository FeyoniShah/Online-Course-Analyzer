# 🎓 Online Course Performance Analyzer

An intuitive desktop-based tool built with **Python**, **Tkinter**, and **MySQL**, designed to help educational institutions track and manage course performance.  
Admins can manage courses, modules, and grades. Students can view progress and generate performance reports.

---

## 🚀 Features

### 👩‍🏫 Admin Dashboard
- View all courses and instructors
- Add new courses and modules
- Enroll students into courses
- Update student grades
- View student details and progress
- Generate performance reports
- View modules under specific courses

### 👩‍🎓 Student Dashboard
- View enrolled courses
- See detailed grades per module
- Visualize progress using graphs
- Generate individual performance report

---

## 🧰 Tech Stack

| Layer            | Technology / Tool            | Purpose                               |
|------------------|-------------------------------|----------------------------------------|
| **Language**      | Python                        | Core programming logic                 |
| **UI Framework**  | Tkinter (built-in)            | Building desktop GUI                   |
| **Database**      | MySQL                         | Storing course, student, and grade data|
| **DB Connector**  | mysql-connector-python        | Python to MySQL connectivity           |
| **Data Handling** | Pandas                        | Calculating averages, completion %     |
| **Graphs**        | Matplotlib                    | Visualizing progress with charts       |
| **Data Structures** | Lists, Dictionaries (nested) | Managing in-memory student/course data |

---

## 📁 Project Structure

```plaintext
online_course_analyzer/
├── main.py           # Entry point with role-based login and dashboard launching
├── admin.py          # Admin GUI and functionalities
├── student.py        # Student GUI and functionalities
├── database.py       # MySQL connectivity and operations     
└── README.md         # Project documentation
