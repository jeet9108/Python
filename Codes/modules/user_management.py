from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import sys
import mysql.connector

path = os.path.dirname(os.path.abspath(__file__))

def connect():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="ca"
    )

def setup_db():
    try:
        db = connect()
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(50) PRIMARY KEY, company_name VARCHAR(150), email VARCHAR(100))")
        db.commit()
        db.close()
    except Exception as e: print(f"DB Error: {e}")

def get_state():
    if window.state() == 'zoomed': return 'zoomed'
    return window.geometry()

def back():
    st = get_state()
    window.destroy()
    os.system(f'python "{os.path.join(path, "dashboard.py")}" --window-state "{st}"')

def load_data():
    try:
        db = connect()
        cur = db.cursor()
        cur.execute("SELECT user_id, company_name, email FROM users ORDER BY user_id")
        rows = cur.fetchall()
        db.close()
        if rows:
            for i, (uid, comp, mail) in enumerate(rows):
                bg = "#f9f9f9" if i % 2 == 0 else "white"
                row = Frame(table)
                row.pack(fill=X)
                Label(row, text=str(uid), font=("Arial", 10), width=15, anchor="w").pack(side=LEFT, padx=5, pady=4)
                Label(row, text=str(comp), font=("Arial", 10),width=25, anchor="w").pack(side=LEFT, padx=5, pady=4)
                Label(row, text=str(mail), font=("Arial", 10),width=25, anchor="w").pack(side=LEFT, padx=5, pady=4)
            cnt_lbl.config(text=f"Total Users: {len(rows)}")
        else:
            Label(table, text="No users found.", font=("Arial", 11), bg="white", fg="#bdc3c7").pack(pady=30)
            cnt_lbl.config(text="Total Users: 0")
    except Exception as e: messagebox.showerror("Error", f"Load failed: {e}")

def add_user():
    win = Toplevel(window)
    win.title("Add User")
    win.geometry("420x320")
    win.config(bg="#ecf0f1")
    win.grab_set()

    def save():
        uid, comp, mail = e1.get().strip(), e2.get().strip(), e3.get().strip()
        if not uid or not comp or not mail:
            messagebox.showerror("Error", "All fields required", parent=win)
            return
        try:
            db = connect()
            cur = db.cursor()
            cur.execute("INSERT INTO users (user_id, company_name, email) VALUES (%s, %s, %s)", (uid, comp, mail))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "User added", parent=win)
            win.destroy()
            load_data()
        except Exception as e: messagebox.showerror("Error", f"Failed: {e}", parent=win)

    form = Frame(win, bg="white", bd=2, relief=GROOVE)
    form.pack(padx=20, pady=20, fill=BOTH, expand=True)

    Label(form, text="User ID:", bg="white").place(x=30, y=30)
    e1 = Entry(form, width=25)
    e1.place(x=150, y=30)

    Label(form, text="Company:", bg="white").place(x=30, y=80)
    e2 = Entry(form, width=25)
    e2.place(x=150, y=80)

    Label(form, text="Email:", bg="white").place(x=30, y=130)
    e3 = Entry(form, width=25)
    e3.place(x=150, y=130)

    Button(form, text="Save", bg="#27ae60", fg="white", width=10, command=save).place(x=100, y=180)
    Button(form, text="Cancel", bg="#e74c3c", fg="white", width=10, command=win.destroy).place(x=220, y=180)

window = Tk()
window.title("AuditPro - Users")
window.geometry("1000x700")

if '--window-state' in sys.argv:
    idx = sys.argv.index('--window-state')
    if idx + 1 < len(sys.argv):
        st = sys.argv[idx + 1]
        if st == 'zoomed': window.state('zoomed')
        else: window.geometry(st)

setup_db()

side = Frame(window, bg="#2c3e50", width=250)
side.pack(side=LEFT, fill=Y)
side.pack_propagate(False)

# Logo
try:
    log_path = os.path.join(path, "..", "..", "Images", "img3.jpeg")
    log_img = Image.open(log_path).resize((150, 100))
    log_photo = ImageTk.PhotoImage(log_img)
    logo = Label(side, image=log_photo, bg="#2c3e50")
    logo.image = log_photo
except:
    logo = Label(side, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
logo.pack(pady=20)


Button(side, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=back).pack(pady=5)

main = Frame(window, bg="#ecf0f1")
main.pack(side=LEFT, fill=BOTH, expand=True)

title = Label(main, text="User Management", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
title.place(x=50, y=40)

bar = Frame(main, bg="#ecf0f1")
bar.place(x=50, y=95, relwidth=0.85)

cnt_lbl = Label(bar, text="Total Users: 0", font=("Arial Black", 11), bg="#ecf0f1", fg="#7f8c8d")
cnt_lbl.pack(side=LEFT)

Button(bar, text="+ Add User", bg="grey", fg="white", font=("Arial Black", 11, "bold"), command=add_user).pack(side=RIGHT)

box = Frame(main, bg="white", bd=1, relief=SOLID)
box.place(x=50, y=135, relwidth=0.85, height=420)

head = Frame(box, bg="#2c3e50")
head.pack(fill=X)
Label(head, text="User ID", fg="white", bg="#2c3e50", width=15, anchor="w").pack(side=LEFT, padx=5, pady=8)
Label(head, text="Company", fg="white", bg="#2c3e50", width=25, anchor="w").pack(side=LEFT, padx=5, pady=8)
Label(head, text="Email", fg="white", bg="#2c3e50", width=25, anchor="w").pack(side=LEFT, padx=5, pady=8)
table = Frame(box, bg="white")
table.pack(fill=BOTH, expand=True)

load_data()
window.mainloop()