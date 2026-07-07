
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import csv
from datetime import date

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Divit@3105",
    database="student_db"
)

cursor = conn.cursor()

selected_id = None


# Add Student
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showerror("Error", "All fields are required")
        return

    sql = """
    INSERT INTO students(name, age, course)
    VALUES(%s,%s,%s)
    """

    values = (name, age, course)

    cursor.execute(sql, values)
    conn.commit()

    view_students()

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Success",
        "Student Added Successfully!"
    )


# View Students
def view_students():

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert("", tk.END, values=row)


# Select Row
def select_record(event):
    global selected_id

    selected = tree.focus()
    values = tree.item(selected, "values")

    if values:
        selected_id = values[0]

        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        age_entry.insert(0, values[2])
        course_entry.insert(0, values[3])


# Update Student
def update_student():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Please select a student to update")
        return

    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showerror("Error", "All fields are required")
        return

    sql = "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s"
    values = (name, age, course, selected_id)

    cursor.execute(sql, values)
    conn.commit()

    view_students()

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Student Updated Successfully!")


# Delete Student
def delete_student():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Please select a student to delete")
        return

    sql = "DELETE FROM students WHERE id=%s"
    cursor.execute(sql, (selected_id,))
    conn.commit()

    view_students()

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Student Deleted Successfully!")
# Export to CSV

def export_students_csv():

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["ID", "Name", "Age", "Course"]
        )

        writer.writerows(rows)

    messagebox.showinfo(
        "Success",
        "Students exported successfully!"
    )
# Attendance Window
def attendance_window():

    attendance_win = tk.Toplevel(root)

    attendance_win.title("Attendance Management")
    attendance_win.geometry("700x500")

    attendance_tree = ttk.Treeview(
        attendance_win,
        columns=(
            "Attendance ID",
            "Student ID",
            "Name",
            "Date",
            "Status"
        ),
        show="headings"
    )

    for col in (
        "Attendance ID",
        "Student ID",
        "Name",
        "Date",
        "Status"
    ):
        attendance_tree.heading(col, text=col)

    attendance_tree.pack(fill=tk.BOTH, expand=True)

    def load_attendance():

        cursor.execute(
            "SELECT * FROM attendance"
        )

        rows = cursor.fetchall()

        attendance_tree.delete(
            *attendance_tree.get_children()
        )

        for row in rows:
            attendance_tree.insert(
                "",
                tk.END,
                values=row
            )

    def mark_present():

        global selected_id

        if selected_id is None:
            messagebox.showerror(
                "Error",
                "Select a student first"
            )
            return

        selected = tree.focus()

        data = tree.item(
            selected,
            "values"
        )

        cursor.execute(
            """
            INSERT INTO attendance
            (
                student_id,
                student_name,
                attendance_date,
                status
            )
            VALUES(%s,%s,%s,%s)
            """,
            (
                data[0],
                data[1],
                date.today(),
                "Present"
            )
        )

        conn.commit()

        load_attendance()

    def mark_absent():

        global selected_id

        if selected_id is None:
            messagebox.showerror(
                "Error",
                "Select a student first"
            )
            return

        selected = tree.focus()

        data = tree.item(
            selected,
            "values"
        )

        cursor.execute(
            """
            INSERT INTO attendance
            (
                student_id,
                student_name,
                attendance_date,
                status
            )
            VALUES(%s,%s,%s,%s)
            """,
            (
                data[0],
                data[1],
                date.today(),
                "Absent"
            )
        )

        conn.commit()

        load_attendance()

    def export_attendance():

        cursor.execute(
            "SELECT * FROM attendance"
        )

        rows = cursor.fetchall()

        with open(
            "attendance.csv",
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Attendance ID",
                    "Student ID",
                    "Name",
                    "Date",
                    "Status"
                ]
            )

            writer.writerows(rows)

        messagebox.showinfo(
            "Success",
            "Attendance exported!"
        )
    def clear_attendance():

        confirm = messagebox.askyesno(
            "Confirm",
            "Clear all attendance records?"
        )

        if confirm:

            cursor.execute(
                "DELETE FROM attendance"
            )

            conn.commit()

            load_attendance()

            messagebox.showinfo(
                "Success",
                "Attendance Cleared!"
            )
    button_frame = ttk.Frame(
        attendance_win
    )

    button_frame.pack(pady=10)

    ttk.Button(
        button_frame,
        text="Present",
        command=mark_present
    ).pack(side=tk.LEFT, padx=5)

    ttk.Button(
        button_frame,
        text="Absent",
        command=mark_absent
    ).pack(side=tk.LEFT, padx=5)

    ttk.Button(
        button_frame,
        text="Export Attendance",
        command=export_attendance
    ).pack(side=tk.LEFT, padx=5)
    ttk.Button(
        button_frame,
        text="Clear Attendance",
        command=clear_attendance
    ).pack(side=tk.LEFT, padx=5)
    load_attendance()




def login():

    login_window = tk.Tk()

    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(
        login_window,
        text="Student Management Login",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tk.Label(login_window, text="Username").pack()

    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()

    password_entry = tk.Entry(
        login_window,
        show="*"
    )
    password_entry.pack()

    def check_login():

        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "1234":

            login_window.destroy()

            root.deiconify()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Username or Password"
            )

    tk.Button(
        login_window,
        text="Login",
        command=check_login
    ).pack(pady=20)

    login_window.mainloop()
# Create GUI
root = tk.Tk()
root.withdraw()
root.title("Student Database Management")
root.geometry("600x500")

# Input Frame
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)

ttk.Label(input_frame, text="Name:").pack(side=tk.LEFT, padx=5)
name_entry = ttk.Entry(input_frame, width=15)
name_entry.pack(side=tk.LEFT, padx=5)

ttk.Label(input_frame, text="Age:").pack(side=tk.LEFT, padx=5)
age_entry = ttk.Entry(input_frame, width=10)
age_entry.pack(side=tk.LEFT, padx=5)

ttk.Label(input_frame, text="Course:").pack(side=tk.LEFT, padx=5)
course_entry = ttk.Entry(input_frame, width=15)
course_entry.pack(side=tk.LEFT, padx=5)

# Button Frame
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill=tk.X)

add_btn = ttk.Button(button_frame, text="Add Student", command=add_student)
add_btn.pack(side=tk.LEFT, padx=5)

update_btn = ttk.Button(button_frame, text="Update", command=update_student)
update_btn.pack(side=tk.LEFT, padx=5)

delete_btn = ttk.Button(button_frame, text="Delete", command=delete_student)
delete_btn.pack(side=tk.LEFT, padx=5)

attendance_btn = ttk.Button(
    button_frame,
    text="Attendance",
    command=attendance_window
)

attendance_btn.pack(
    side=tk.LEFT,
    padx=5
)

export_btn = ttk.Button(
    button_frame,
    text="Export Students",
    command=export_students_csv
)

export_btn.pack(
    side=tk.LEFT,
    padx=5
)

# Table Frame
table_frame = ttk.Frame(root, padding="10")
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "Name", "Age", "Course")
tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", select_record)

view_students()

login()

root.mainloop()
conn.close()
       

