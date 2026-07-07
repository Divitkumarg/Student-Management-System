import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="student_db"
)

cursor = conn.cursor()

# Add Student Function
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

    messagebox.showinfo("Success", "Student Added Successfully")

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

# Main Window
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x350")

# Heading
title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

# Name
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack()

# Age
tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root, width=30)
age_entry.pack()

# Course
tk.Label(root, text="Course").pack()
course_entry = tk.Entry(root, width=30)
course_entry.pack()

# Button
tk.Button(
    root,
    text="Add Student",
    command=add_student,
    width=20
).pack(pady=20)
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Course"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.pack(pady=10)
def view_students():

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert("", tk.END, values=row)

      

tk.Button(
    root,
    text="View Students",
    command=view_students
).pack()

root.mainloop()