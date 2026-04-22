from tkinter import *
import webbrowser
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

def open_phpmyadmin():
    """Open phpMyAdmin directly in the user's default browser."""
    webbrowser.open("http://localhost/phpmyadmin/index.php?route=/database/structure&db=ca")

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

# Content area
content_area = Frame(window, bg="#ecf0f1")
content_area.pack(side=LEFT, fill=BOTH, expand=True)

lbl_title = Label(content_area, text="Database Manager", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
lbl_title.place(x=50, y=40)

# Form Frame for the button
form_frame = Frame(content_area, bg="white", bd=2, relief=GROOVE)
form_frame.place(x=50, y=100, width=600, height=300)

lbl_info = Label(form_frame, text="Managed the 'ca' database structure via phpMyAdmin", font=("Arial Black", 14), bg="white", fg="#2c3e50")
lbl_info.place(relx=0.5, y=50, anchor=CENTER)

icon_label = Label(form_frame, text="🌐", font=("Arial", 48), bg="white", fg="#f39c12")
icon_label.place(relx=0.5, y=120, anchor=CENTER)

btn_open = Button(form_frame, text="Open phpMyAdmin", bg="#f39c12", fg="white", font=("Arial Black", 14, "bold"), width=30, pady=5, command=open_phpmyadmin)
btn_open.place(relx=0.5, y=200, anchor=CENTER)

window.mainloop()
