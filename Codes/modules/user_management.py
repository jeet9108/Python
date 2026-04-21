from tkinter import *
from tkinter import messagebox
import mysql.connector
import os
import sys

def get_window_state():
    """Get the current window state to pass to the next module."""
    if window.state() == 'zoomed':
        return 'zoomed'
    else:
        return window.geometry()

def go_back():
    state = get_window_state()
    window.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(script_dir, "dashboard.py")}" --window-state "{state}"')

def Register():
    Id = e1.get()
    Name = e2.get()
    Role = e3.get()
    Email = e4.get()
    
    if(Id!= "" and Name!="" and Role!="" and Email != ""):
        try:
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="ca")
            mycursor = mydb.cursor()
            Insert = "Insert into users(id, name, role, email) values(%s,%s,%s,%s)"
            Value = (Id, Name, Role, Email)
            mycursor.execute(Insert, Value)
            mydb.commit()
            messagebox.askokcancel("Information", "Record inserted")
            Clear()
        except Exception as e:
            messagebox.showinfo("Error", f"Database error: {e}")
    else:
        messagebox.askokcancel("Information", "New Entry Fill All Details")

def Clear():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

window = Tk()
window.title("AuditPro - User Management")
window.geometry("1000x700")

# Restore window state from command-line argument
if '--window-state' in sys.argv:
    idx = sys.argv.index('--window-state')
    if idx + 1 < len(sys.argv):
        state = sys.argv[idx + 1]
        if state == 'zoomed':
            window.state('zoomed')
        else:
            window.geometry(state)

# Sidebar
sidebar = Frame(window, bg="#2c3e50", width=250)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

lbl_logo = Label(sidebar, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
lbl_logo.pack(pady=30)

lbl_role = Label(sidebar, text="Role: Admin", bg="#2c3e50", fg="#bdc3c7", font=("Arial Black", 10))
lbl_role.pack(pady=10)

btn_back = Button(sidebar, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=go_back)
btn_back.pack(pady=5)

# Content 
content_area = Frame(window, bg="#ecf0f1")
content_area.pack(side=LEFT, fill=BOTH, expand=True)

lbl_title = Label(content_area, text="User Management", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
lbl_title.place(x=50, y=40)

# User registration form
form_frame = Frame(content_area, bg="white", bd=2, relief=GROOVE)
form_frame.place(x=50, y=100, width=600, height=400)

label1 = Label(form_frame, text="User ID", width=20, height=2, bg="pink")
label1.grid(row=0, column=0, pady=10, padx=10)
label2 = Label(form_frame, text="Name", width=20, height=2, bg="pink")
label2.grid(row=1, column=0, pady=10, padx=10)
label3 = Label(form_frame, text="Role", width=20, height=2, bg="pink")
label3.grid(row=2, column=0, pady=10, padx=10)
label4 = Label(form_frame, text="Email", width=20, height=2, bg="pink")
label4.grid(row=3, column=0, pady=10, padx=10)

e1 = Entry(form_frame, width=30, borderwidth=8)
e1.grid(row=0, column=1)
e2 = Entry(form_frame, width=30, borderwidth=8)
e2.grid(row=1, column=1)
e3 = Entry(form_frame, width=30, borderwidth=8)
e3.grid(row=2, column=1)
e4 = Entry(form_frame, width=30, borderwidth=8)
e4.grid(row=3, column=1)

button1 = Button(form_frame, text="Register", width=10, height=2, bg="#3498db", fg="white", font=("Arial Black", 10), command=Register)
button1.grid(row=4, column=0, pady=20)
button2 = Button(form_frame, text="Clear", width=10, height=2, bg="#e74c3c", fg="white", font=("Arial Black", 10), command=Clear)
button2.grid(row=4, column=1, pady=20)

window.mainloop()
