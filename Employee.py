import tkinter as tk
from tkinter import messagebox
 
# Employee class
class Employee:
    def __init__(self, name, position, pay_rate):
        self.name = name
        self.position = position
        self.pay_rate = pay_rate
 
    def calc_netpay(self, hrs_worked):
        net_pay = self.pay_rate * hrs_worked
        return net_pay
 
# Function to open second window for employee entry
def open_employee_form():
    form = tk.Toplevel(window)
    form.title("Employee Entry")
    form.geometry("300x300")
 
    # Labels and Entry fields
    tk.Label(form, text="Name").place(x=20, y=20)
    entry_name = tk.Entry(form)
    entry_name.place(x=120, y=20)
 
    tk.Label(form, text="Position").place(x=20, y=60)
    entry_position = tk.Entry(form)
    entry_position.place(x=120, y=60)
 
    tk.Label(form, text="Pay Rate").place(x=20, y=100)
    entry_payrate = tk.Entry(form)
    entry_payrate.place(x=120, y=100)
 
    tk.Label(form, text="Hours Worked").place(x=20, y=140)
    entry_hours = tk.Entry(form)
    entry_hours.place(x=120, y=140)
 
    # Submit button
    def submit_data():
        try:
            name = entry_name.get()
            position = entry_position.get()
            pay_rate = float(entry_payrate.get())
            hours = float(entry_hours.get())
 
            emp = Employee(name, position, pay_rate)
            net_pay = emp.calc_netpay(hours)
 
            # Save to file
            with open("employees.txt", "a") as file:
                file.write(f"name: {name}\nposition: {position}\npay rate: {pay_rate}\nhours worked: {hours}\nnet pay: {net_pay}\n\n")
 
            messagebox.showinfo("Success", f"Net Pay: ${net_pay:.2f} saved.")
            form.destroy()
 
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for pay rate and hours.")
 
    tk.Button(form, text="Submit", command=submit_data).place(x=100, y=200)
 
# Quit program
def quit_program():
    messagebox.showinfo("Exit", "Thanks for using this program")
    window.destroy()
 
# Main window
window = tk.Tk()
window.title("Employee Entry System")
window.geometry("300x150")
 
tk.Label(window, text="Do you want to add employees?").place(x=40, y=20)
 
tk.Button(window, text="Yes", width=10, command=open_employee_form).place(x=50, y=60)
tk.Button(window, text="No", width=10, command=quit_program).place(x=150, y=60)
 
window.mainloop()