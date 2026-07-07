username = input("Enter Username: ")
password = input("Enter Password: ")

if username != "admin" or password != "1234":
    print("Invalid Login!")
    exit()

print("Login Successful!")
import csv

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Divit@3105",
    database="student_db"
)

cursor = conn.cursor()

while True:
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Update Student")
    print("6. Export to CSV")
    print("7. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        course = input("Enter Course: ")

        sql = "INSERT INTO students(name, age, course) VALUES(%s,%s,%s)"
        val = (name, age, course)

        cursor.execute(sql, val)
        conn.commit()

        print("Student Added Successfully!")

    elif choice == "2":
        cursor.execute("SELECT * FROM students")

        records = cursor.fetchall()

        print("\nStudent Records")
        print("\nID\tNAME\t\tAGE\tCOURSE")
        print("-" * 50)

        for row in records:
         print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
        

    elif choice == "3":
        name = input("Enter Student Name: ")

        cursor.execute(
            "SELECT * FROM students WHERE name=%s",
            (name,)
        )

        result = cursor.fetchall()

        for row in result:
            print(row)

    elif choice == "4":
        student_id = int(input("Enter Student ID: "))

        cursor.execute(
            "DELETE FROM students WHERE id=%s",
            (student_id,)
        )

        conn.commit()

        print("Student Deleted Successfully!")

    elif choice == "5":
     student_id = int(input("Enter Student ID: "))

     new_name = input("Enter New Name: ")
     new_age = int(input("Enter New Age: "))
     new_course = input("Enter New Course: ")

     sql = """
     UPDATE students
     SET name=%s, age=%s, course=%s
     WHERE id=%s
     """

     values = (new_name, new_age, new_course, student_id)

     cursor.execute(sql, values)
     conn.commit()

     print("Student Updated Successfully!")

    elif choice == "6":
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        with open("students.csv", "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["ID", "Name", "Age", "Course"])

            for row in records:
                writer.writerow(row)

        print("Data Exported Successfully!")

    elif choice == "7":
        print("Thank You!")
        break    

    else:
        print("Invalid Choice")