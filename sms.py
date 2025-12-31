
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ---------- DB CONNECTION ----------
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Krishna@1705",
            database="58r",
            port=3306
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


# ---------- CRUD FUNCTIONS ----------
def add_student():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    course = entry_course.get().strip()

    if not name or not age or not course:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
            (name, age, course)
        )
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        clear_form()
        load_students()
    finally:
        conn.close()


def load_students():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)


def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a student")
        return

    student_id = tree.item(selected)["values"][0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Student removed")
    load_students()


def select_student(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)

    entry_name.insert(0, values[1])
    entry_age.insert(0, values[2])
    entry_course.insert(0, values[3])


def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student to update")
        return

    student_id = tree.item(selected)["values"][0]
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
        (name, age, course, student_id)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Updated", "Student updated successfully")
    load_students()


def search_student():
    keyword = entry_search.get()

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM students WHERE name LIKE %s OR course LIKE %s",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)


def clear_form():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)


# ---------- GUI ----------
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x550")

title = tk.Label(root, text="Student Management System",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

# Form
form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(form)
entry_name.grid(row=0, column=1)

tk.Label(form, text="Age").grid(row=1, column=0, padx=5, pady=5)
entry_age = tk.Entry(form)
entry_age.grid(row=1, column=1)

tk.Label(form, text="Course").grid(row=2, column=0, padx=5, pady=5)
entry_course = tk.Entry(form)
entry_course.grid(row=2, column=1)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=12, command=add_student,
          bg="green", fg="white").grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Update", width=12, command=update_student,
          bg="orange", fg="white").grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Delete", width=12, command=delete_student,
          bg="red", fg="white").grid(row=0, column=2, padx=5)

# Search
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

entry_search = tk.Entry(search_frame, width=25)
entry_search.grid(row=0, column=0, padx=5)
tk.Button(search_frame, text="Search", command=search_student).grid(row=0, column=1)

# Table
tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Course"),
                    show="headings")
tree.pack(fill=tk.BOTH, expand=True, pady=10)

for col in ("ID", "Name", "Age", "Course"):
    tree.heading(col, text=col)

tree.bind("<ButtonRelease-1>", select_student)

load_students()
root.mainloop()
