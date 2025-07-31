import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

#File path
USER_DATA_FILE = 'users.json'
STUDENT_DATA_FILE = 'student.json'


#Account class
class Account:
    def __init__(self, username: str, password: str):
        self.username = username.strip()
        self.password = password.strip()

#Judge the account if valid
    def is_valid(self):
        return bool(self.username and self.password)

    def to_dict(self):
        return {self.username: self.password}

#Student class
class Student:
    def __init__(self, name: str, student_id: str, course_name: str, course_code: str):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.course_name = course_name.strip()
        self.course_code = course_code.strip()

    def is_valid(self):
        return all([self.name, self.student_id, self.course_name, self.course_code])

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.student_id,
            "course_name": self.course_name,
            "course_code": self.course_code
        }
    
# Check if the file exist
def load_json_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return [] if file_path == STUDENT_DATA_FILE else {}
    return [] if file_path == STUDENT_DATA_FILE else {}


def save_json_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# setup main Tkinter window
# Login/Sign up page
def main_app():
    root = tk.Tk()
    root.title("Student Management System")
    root.geometry("300x150")

    tk.Label(root, text="Welcome! Please login or sign up").pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Login", width=15, command=lambda: [root.destroy(), show_login()]).pack(pady=5)
    tk.Button(btn_frame, text="Signup", width=15, command=lambda: [root.destroy(), show_signup()]).pack(pady=5)

    # Create user or student data files with default content if the file don't exist.
    if not os.path.exists(USER_DATA_FILE):
        save_json_file({}, USER_DATA_FILE)
    if not os.path.exists(STUDENT_DATA_FILE):
        save_json_file([], STUDENT_DATA_FILE)

    root.mainloop()

#Sign up page
def show_signup():
    win = tk.Tk()
    win.title("Signup")
    win.geometry("300x200")

    tk.Label(win, text="Username").pack(pady=5)
    username_entry = tk.Entry(win)
    username_entry.pack(pady=5)

    tk.Label(win, text="Password").pack(pady=5)
    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

#check if the inputs is valid
    def signup():
        acc = Account(username_entry.get(), password_entry.get())
        if not acc.is_valid():
            messagebox.showerror("Error", "Please enter both username and password")
            return

        users = load_json_file(USER_DATA_FILE)
        if acc.username in users:
            messagebox.showerror("Error", "Username already exists!")
            return

        users.update(acc.to_dict())
        save_json_file(users, USER_DATA_FILE)
        messagebox.showinfo("Success", "Signup successful! You can now login.")
        win.destroy()
        main_app()

    tk.Button(win, text="Signup", command=signup).pack(pady=20)
    win.mainloop()

#Login page
def show_login():
    win = tk.Tk()
    win.title("Login")
    win.geometry("300x200")

    tk.Label(win, text="Username").pack(pady=5)
    username_entry = tk.Entry(win)
    username_entry.pack(pady=5)

    tk.Label(win, text="Password").pack(pady=5)
    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

#Check if the input matches data in the account file 
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        users = load_json_file(USER_DATA_FILE)
        if users.get(username) == password:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            win.destroy()
            show_student_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    tk.Button(win, text="Login", command=login).pack(pady=20)
    win.mainloop()

#Student dashboard
def show_student_dashboard(username):
    students = load_json_file(STUDENT_DATA_FILE)

    win = tk.Tk()
    win.title(f"All Students - Logged in as {username}")
    win.geometry("600x400")

    tk.Label(win, text="Student Records", font=('Helvetica', 14)).pack(pady=10)

#Title for each column
    tree = ttk.Treeview(win, columns=("Name", "ID", "Course", "Code"), show='headings')
    for col in ("Name", "ID", "Course", "Code"):
        tree.heading(col, text=col)
        tree.column(col, width=150 if col != "ID" else 100)
    tree.pack(pady=10, fill='both', expand=True, padx=20)

#Load students from the in-memory list into the Treeview
    def load_students():
        tree.delete(*tree.get_children())
        for stu in students:
            tree.insert('', tk.END, values=(
                stu.get('name', ''),
                stu.get('id', ''),
                stu.get('course_name', ''),
                stu.get('course_code', '')
            ))

#add student page
    def open_add_student():
        add_win = tk.Toplevel(win)
        add_win.title("Add Student")
        add_win.geometry("350x300")

        fields = ["Name", "ID", "Course Name", "Course Code"]
        entries = {}

        for idx, field in enumerate(fields):
            tk.Label(add_win, text=f"{field}:").grid(row=idx, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(add_win)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky='we')
            entries[field.lower().replace(' ', '_')] = entry

        def save_student():
            stu = Student(
                entries['name'].get(),
                entries['id'].get(),
                entries['course_name'].get(),
                entries['course_code'].get()
            )
            if not stu.is_valid():
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            #Save the new data into the file
            students.append(stu.to_dict())
            save_json_file(students, STUDENT_DATA_FILE)
            messagebox.showinfo("Success", "Student added successfully!")
            add_win.destroy()
            load_students()

        btn_frame = tk.Frame(add_win)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Save", command=save_student).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=add_win.destroy).pack(side='left', padx=5)

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add Student", command=open_add_student).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Logout", command=lambda: [win.destroy(), main_app()]).pack(side='right', padx=5)


     #Tkinter loop
    load_students()
    win.mainloop()

if __name__ == "__main__":
    main_app()
