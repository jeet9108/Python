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

def test_connection():
    try:
        host_val = e_host.get()
        user_val = e_user.get()
        pass_val = e_pass.get()
        
        mydb = mysql.connector.connect(
            host=host_val,
            user=user_val,
            password=pass_val
        )
        if mydb:
            messagebox.showinfo("Success", "Connection Established Successfully")
            mydb.close()
    except Exception as e:
        messagebox.showerror("Error", f"Connection Error: {e}")

window = Tk()
window.title("AuditPro - Database Manager")
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

lbl_title = Label(content_area, text="Database Manager", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
lbl_title.place(x=50, y=40)

# Form
form_frame = Frame(content_area, bg="white", bd=2, relief=GROOVE)
form_frame.place(x=50, y=100, width=500, height=350)

lbl_host = Label(form_frame, text="Host:", font=("Arial Black", 11), bg="white")
lbl_host.place(x=50, y=50)
e_host = Entry(form_frame, width=25)
e_host.insert(0, "localhost")
e_host.place(x=180, y=50)

lbl_user = Label(form_frame, text="User:", font=("Arial Black", 11), bg="white")
lbl_user.place(x=50, y=100)
e_user = Entry(form_frame, width=25)
e_user.insert(0, "root")
e_user.place(x=180, y=100)

lbl_pass = Label(form_frame, text="Password:", font=("Arial Black", 11), bg="white")
lbl_pass.place(x=50, y=150)
e_pass = Entry(form_frame, width=25, show="*")
e_pass.place(x=180, y=150)

btn_test = Button(form_frame, text="Test Connection", bg="#3498db", fg="white", font=("Arial Black", 11, "bold"), width=15, command=test_connection)
btn_test.place(x=150, y=220)

window.mainloop()
