from tkinter import *
from tkinter import messagebox
import os
import sys
import mysql.connector

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_db_connection():
    """Get a MySQL database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ca"
    )

def ensure_users_table():
    """Create the users table if it doesn't exist."""
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(50) PRIMARY KEY,
                company_name VARCHAR(150),
                email VARCHAR(100)
            )
        """)
        con.commit()
        con.close()
    except Exception as e:
        print(f"Error creating users table: {e}")

def get_window_state():
    """Get the current window state to pass to the next module."""
    if window.state() == 'zoomed':
        return 'zoomed'
    else:
        return window.geometry()

def go_back():
    state = get_window_state()
    window.destroy()
    os.system(f'python "{os.path.join(script_dir, "dashboard.py")}" --window-state "{state}"')

def load_users():
    """Load all users from the database and display in the table."""
    # Clear existing rows
    for widget in table_body_frame.winfo_children():
        widget.destroy()

    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT user_id, company_name, email FROM users ORDER BY user_id")
        rows = cursor.fetchall()
        con.close()

        if rows:
            for i, (uid, company, email) in enumerate(rows):
                row_bg = "#f9f9f9" if i % 2 == 0 else "white"
                row_frame = Frame(table_body_frame, bg=row_bg)
                row_frame.pack(fill=X)

                Label(row_frame, text=str(uid), font=("Arial", 10), bg=row_bg, fg="#2c3e50",
                      width=15, anchor="w").pack(side=LEFT, padx=5, pady=4)
                Label(row_frame, text=str(company), font=("Arial", 10), bg=row_bg, fg="#2c3e50",
                      width=25, anchor="w").pack(side=LEFT, padx=5, pady=4)
                Label(row_frame, text=str(email), font=("Arial", 10), bg=row_bg, fg="#2c3e50",
                      width=25, anchor="w").pack(side=LEFT, padx=5, pady=4)

            # Update count label
            lbl_count.config(text=f"Total Users: {len(rows)}")
        else:
            Label(table_body_frame, text="No users found in the database.", font=("Arial", 11),
                  bg="white", fg="#bdc3c7").pack(pady=30)
            lbl_count.config(text="Total Users: 0")

    except Exception as e:
        messagebox.showerror("Database Error", f"Could not load users: {e}")

def open_add_user_dialog():
    """Open a dialog window to add a new user."""
    dialog = Toplevel(window)
    dialog.title("Add New User")
    dialog.geometry("420x320")
    dialog.config(bg="#ecf0f1")
    dialog.resizable(False, False)
    dialog.grab_set()  # Make it modal

    # Center the dialog on the main window
    dialog.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() // 2) - 210
    y = window.winfo_y() + (window.winfo_height() // 2) - 160
    dialog.geometry(f"420x320+{x}+{y}")

    # Title
    Label(dialog, text="Register New User", font=("Arial Black", 16, "bold"),
          bg="#ecf0f1", fg="#2c3e50").pack(pady=(20, 10))

    # Form frame
    form = Frame(dialog, bg="white", bd=2, relief=GROOVE)
    form.pack(padx=20, pady=5, fill=BOTH, expand=True)

    # User ID
    Label(form, text="User ID:", font=("Arial Black", 11), bg="white").place(x=30, y=25)
    e_user_id = Entry(form, width=25, font=("Arial", 11))
    e_user_id.place(x=170, y=25)

    # Company Name
    Label(form, text="Company Name:", font=("Arial Black", 11), bg="white").place(x=30, y=70)
    e_company = Entry(form, width=25, font=("Arial", 11))
    e_company.place(x=170, y=70)

    # Email
    Label(form, text="Email:", font=("Arial Black", 11), bg="white").place(x=30, y=115)
    e_email = Entry(form, width=25, font=("Arial", 11))
    e_email.place(x=170, y=115)

    # Status label for feedback
    status_label = Label(form, text="", font=("Arial", 10), bg="white")
    status_label.place(relx=0.5, y=155, anchor="center")

    def register_user():
        user_id = e_user_id.get().strip()
        company = e_company.get().strip()
        email = e_email.get().strip()

        if not user_id or not company or not email:
            messagebox.showerror("Error", "All fields are required!", parent=dialog)
            return

        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, company_name, email) VALUES (%s, %s, %s)",
                (user_id, company, email)
            )
            con.commit()
            con.close()

            messagebox.showinfo("Success", f"User '{user_id}' registered successfully!", parent=dialog)
            dialog.destroy()
            load_users()  # Refresh the table

        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", f"User ID '{user_id}' already exists!", parent=dialog)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not register user: {e}", parent=dialog)

    def cancel():
        dialog.destroy()

    # Buttons
    btn_frame = Frame(form, bg="white")
    btn_frame.place(relx=0.5, y=195, anchor="center")

    Button(btn_frame, text="Register", bg="#27ae60", fg="white", font=("Arial Black", 11, "bold"),
           width=12, command=register_user).pack(side=LEFT, padx=10)
    Button(btn_frame, text="Cancel", bg="#e74c3c", fg="white", font=("Arial Black", 11, "bold"),
           width=12, command=cancel).pack(side=LEFT, padx=10)


# ==================== Main Window ====================

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

# Ensure users table exists
ensure_users_table()

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

# Content Area
content_area = Frame(window, bg="#ecf0f1")
content_area.pack(side=LEFT, fill=BOTH, expand=True)

# Title
lbl_title = Label(content_area, text="User Management", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
lbl_title.place(x=50, y=40)

# Count & Add User button row
top_bar = Frame(content_area, bg="#ecf0f1")
top_bar.place(x=50, y=90, relwidth=0.85)

lbl_count = Label(top_bar, text="Total Users: 0", font=("Arial Black", 11), bg="#ecf0f1", fg="#7f8c8d")
lbl_count.pack(side=LEFT)

btn_add_user = Button(top_bar, text="+ Add New User", bg="#27ae60", fg="white",
                      font=("Arial Black", 11, "bold"), padx=15, pady=3, command=open_add_user_dialog)
btn_add_user.pack(side=RIGHT)

# Users Table
table_frame = Frame(content_area, bg="white", bd=1, relief=SOLID)
table_frame.place(x=50, y=130, relwidth=0.85, height=420)

# Table header
header_frame = Frame(table_frame, bg="#2c3e50")
header_frame.pack(fill=X)

Label(header_frame, text="User ID", font=("Arial Black", 10), bg="#2c3e50", fg="white",
      width=15, anchor="w").pack(side=LEFT, padx=5, pady=8)
Label(header_frame, text="Company Name", font=("Arial Black", 10), bg="#2c3e50", fg="white",
      width=25, anchor="w").pack(side=LEFT, padx=5, pady=8)
Label(header_frame, text="Email", font=("Arial Black", 10), bg="#2c3e50", fg="white",
      width=25, anchor="w").pack(side=LEFT, padx=5, pady=8)

# Scrollable table body
table_canvas = Canvas(table_frame, bg="white", highlightthickness=0)
scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=table_canvas.yview)
table_body_frame = Frame(table_canvas, bg="white")

table_body_frame.bind("<Configure>", lambda e: table_canvas.configure(scrollregion=table_canvas.bbox("all")))
table_canvas.create_window((0, 0), window=table_body_frame, anchor="nw")
table_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
table_canvas.pack(fill=BOTH, expand=True)

# Load users from database on startup
load_users()

window.mainloop()