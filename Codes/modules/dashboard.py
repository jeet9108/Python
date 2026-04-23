from tkinter import *
import os
import sys
import mysql.connector

def get_db_connection():
    """Get a MySQL database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ca"
    )

def get_review_counts():
    """Get pending and completed review counts from the database."""
    pending = 0
    completed = 0
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM working_papers WHERE status = 'PENDING'")
        pending = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM working_papers WHERE status = 'ACCEPTED'")
        completed = cursor.fetchone()[0]
        con.close()
    except Exception as e:
        print(f"Database error: {e}")
    return pending, completed

def get_recent_papers():
    """Get recent working papers from the database."""
    papers = []
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT filename, status, created_at FROM working_papers ORDER BY created_at DESC LIMIT 10")
        papers = cursor.fetchall()
        con.close()
    except Exception as e:
        print(f"Database error: {e}")
    return papers

def get_window_state():
    """Get the current window state to pass to the next module."""
    if window.state() == 'zoomed':
        return 'zoomed'
    else:
        return window.geometry()

def open_wp():
    state = get_window_state()
    window.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(script_dir, "working_papers.py")}" --window-state "{state}"')

def open_user_mgmt():
    state = get_window_state()
    window.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(script_dir, "user_management.py")}" --window-state "{state}"')

def open_db():
    state = get_window_state()
    window.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(script_dir, "database_manager.py")}" --window-state "{state}"')

def open_help():
    state = get_window_state()
    window.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(script_dir, "help.py")}" --window-state "{state}"')

def logout():
    state = get_window_state()
    window.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(script_dir, "Login.py")}" --window-state "{state}"')

window = Tk()
window.title("AuditPro")
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

# Get counts from database
pending_count, completed_count = get_review_counts()
recent_papers = get_recent_papers()

sidebar = Frame(window, bg="#2c3e50", width=250)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

lbl_logo = Label(sidebar, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
lbl_logo.pack(pady=30)

lbl_role = Label(sidebar, text="Role: CA_Yogesh_Shah", bg="#2c3e50", fg="#bdc3c7", font=("Arial Black", 10))
lbl_role.pack(pady=10)

btn_dash = Button(sidebar, text="Dashboard", bg="white", font=("Arial Black", 12), width=20)
btn_dash.pack(pady=5)

btn_wp = Button(sidebar, text="Working Papers", bg="white", font=("Arial Black", 12), width=20, command=open_wp)
btn_wp.pack(pady=5)

btn_user_mgmt = Button(sidebar, text="User Management", bg="white", font=("Arial Black", 12), width=20, command=open_user_mgmt)
btn_user_mgmt.pack(pady=5)

btn_db = Button(sidebar, text="Database Manager", bg="white", font=("Arial Black", 12), width=20, command=open_db)
btn_db.pack(pady=5)

btn_help = Button(sidebar, text="Help & Standards", bg="white", font=("Arial Black", 12), width=20, command=open_help)
btn_help.pack(pady=5)

btn_logout = Button(sidebar, text="Logout", bg="#c0392b", fg="white", font=("Arial Black", 10, "bold"), width=20, command=logout)
btn_logout.pack(side=BOTTOM, pady=20)

content_area = Frame(window, bg="#e1f5fe")
content_area.pack(side=LEFT, fill=BOTH, expand=True)


lbl_welcome = Label(content_area, text="Welcome back, CA Yogesh Shah", font=("Arial Black", 24), bg="#e1f5fe", fg="#2c3e50")
lbl_welcome.place(x=50, y=40)

# Cards frame
cards_frame = Frame(content_area, bg="#e1f5fe")
cards_frame.place(relx=0.5, rely=0.18, anchor="center")

card1 = Frame(cards_frame, bg="white", width=250, height=120, bd=1, relief=SOLID)
card1.pack(side=LEFT, padx=50)
card1.pack_propagate(False)

lbl_num1 = Label(card1, text=str(pending_count), font=("Arial Black", 32, "bold"), fg="#e67e22", bg="white")
lbl_num1.place(relx=0.5, rely=0.3, anchor="center")

lbl_txt1 = Label(card1, text="Reviews Pending", font=("Arial Black", 12), fg="gray", bg="white")
lbl_txt1.place(relx=0.5, rely=0.7, anchor="center")

card2 = Frame(cards_frame, bg="white", width=250, height=120, bd=1, relief=SOLID)
card2.pack(side=LEFT, padx=50)
card2.pack_propagate(False)

lbl_num2 = Label(card2, text=str(completed_count), font=("Arial Black", 32, "bold"), fg="#27ae60", bg="white")
lbl_num2.place(relx=0.5, rely=0.3, anchor="center")

lbl_txt2 = Label(card2, text="Reviews Completed", font=("Arial Black", 12), fg="gray", bg="white")
lbl_txt2.place(relx=0.5, rely=0.7, anchor="center")

# Recent Working Papers section
papers_frame = Frame(content_area, bg="white", bd=1, relief=SOLID)
papers_frame.place(x=50, y=220, relwidth=0.85, height=350)

lbl_recent = Label(papers_frame, text="Recent Working Papers", font=("Arial Black", 14), bg="white", fg="#2c3e50")
lbl_recent.pack(pady=10, anchor="w", padx=20)

# Header row
header_frame = Frame(papers_frame, bg="#2c3e50")
header_frame.pack(fill=X, padx=20)

Label(header_frame, text="Filename", font=("Arial Black", 10), bg="#2c3e50", fg="white", width=35, anchor="w").pack(side=LEFT, padx=5, pady=5)
Label(header_frame, text="Status", font=("Arial Black", 10), bg="#2c3e50", fg="white", width=12, anchor="center").pack(side=LEFT, padx=5, pady=5)
Label(header_frame, text="Date", font=("Arial Black", 10), bg="#2c3e50", fg="white", width=18, anchor="center").pack(side=LEFT, padx=5, pady=5)

# Paper rows
if recent_papers:
    for i, (filename, status, created_at) in enumerate(recent_papers):
        row_bg = "#f9f9f9" if i % 2 == 0 else "white"
        row_frame = Frame(papers_frame, bg=row_bg)
        row_frame.pack(fill=X, padx=20)

        Label(row_frame, text=filename, font=("Arial", 10), bg=row_bg, fg="#2c3e50", width=35, anchor="w").pack(side=LEFT, padx=5, pady=4)

        # Status with color
        if status == "ACCEPTED":
            status_fg = "#27ae60"
        elif status == "REJECTED":
            status_fg = "#e74c3c"
        else:
            status_fg = "#e67e22"

        Label(row_frame, text=status, font=("Arial", 10, "bold"), bg=row_bg, fg=status_fg, width=12, anchor="center").pack(side=LEFT, padx=5, pady=4)

        date_str = created_at.strftime("%Y-%m-%d %H:%M") if created_at else ""
        Label(row_frame, text=date_str, font=("Arial", 10), bg=row_bg, fg="#7f8c8d", width=18, anchor="center").pack(side=LEFT, padx=5, pady=4)
else:
    Label(papers_frame, text="No working papers uploaded yet.", font=("Arial", 11), bg="white", fg="#bdc3c7").pack(pady=30)

window.mainloop()