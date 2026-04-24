from tkinter import *
import os
import sys
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="ca"
    )

def get_counts():
    p, c = 0, 0
    try:
        db = connect()
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM working_papers WHERE status = 'PENDING'")
        p = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM working_papers WHERE status = 'ACCEPTED'")
        c = cur.fetchone()[0]
        db.close()
    except Exception as e:
        print(f"Error: {e}")
    return p, c

def get_papers():
    data = []
    try:
        db = connect()
        cur = db.cursor()
        cur.execute("SELECT filename, status, created_at FROM working_papers ORDER BY created_at DESC LIMIT 10")
        data = cur.fetchall()
        db.close()
    except Exception as e:
        print(f"Error: {e}")
    return data

def get_state():
    if window.state() == 'zoomed':
        return 'zoomed'
    return window.geometry()

def goto(script):
    st = get_state()
    window.destroy()
    path = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(path, script)}" --window-state "{st}"')

window = Tk()
window.title("AuditPro")
window.geometry("1000x700")

if '--window-state' in sys.argv:
    idx = sys.argv.index('--window-state')
    if idx + 1 < len(sys.argv):
        st = sys.argv[idx + 1]
        if st == 'zoomed':
            window.state('zoomed')
        else:
            window.geometry(st)

p_cnt, c_cnt = get_counts()
recent = get_papers()

side = Frame(window, bg="#2c3e50", width=250)
side.pack(side=LEFT, fill=Y)
side.pack_propagate(False)

logo = Label(side, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
logo.pack(pady=30)

role = Label(side, text="Role: CA_Yogesh_Shah", bg="#2c3e50", fg="#bdc3c7", font=("Arial Black", 10))
role.pack(pady=10)

btn_dash = Button(side, text="Dashboard", bg="white", font=("Arial Black", 12), width=20)
btn_dash.pack(pady=5)

btn_wp = Button(side, text="Working Papers", bg="white", font=("Arial Black", 12), width=20, command=lambda: goto("working_papers.py"))
btn_wp.pack(pady=5)

btn_user = Button(side, text="User Management", bg="white", font=("Arial Black", 12), width=20, command=lambda: goto("user_management.py"))
btn_user.pack(pady=5)

btn_db = Button(side, text="Database Manager", bg="white", font=("Arial Black", 12), width=20, command=lambda: goto("database_manager.py"))
btn_db.pack(pady=5)

btn_help = Button(side, text="Help", bg="white", font=("Arial Black", 12), width=20, command=lambda: goto("help.py"))
btn_help.pack(pady=5)

btn_out = Button(side, text="Logout", bg="#c0392b", fg="white", font=("Arial Black", 10, "bold"), width=20, command=lambda: goto("Login.py"))
btn_out.pack(side=BOTTOM, pady=20)

main = Frame(window, bg="#e1f5fe")
main.pack(side=LEFT, fill=BOTH, expand=True)

welcome = Label(main, text="Welcome back, CA Yogesh Shah", font=("Arial Black", 24), bg="#e1f5fe", fg="#2c3e50")
welcome.place(x=50, y=40)

cards = Frame(main, bg="#e1f5fe")
cards.place(relx=0.5, rely=0.18, anchor="center")

c1 = Frame(cards, bg="white", width=250, height=120, bd=1, relief=SOLID)
c1.pack(side=LEFT, padx=50)
c1.pack_propagate(False)

n1 = Label(c1, text=str(p_cnt), font=("Arial Black", 32, "bold"), fg="#e67e22", bg="white")
n1.place(relx=0.5, rely=0.3, anchor="center")

t1 = Label(c1, text="Reviews Pending", font=("Arial Black", 12), fg="gray", bg="white")
t1.place(relx=0.5, rely=0.7, anchor="center")

c2 = Frame(cards, bg="white", width=250, height=120, bd=1, relief=SOLID)
c2.pack(side=LEFT, padx=50)
c2.pack_propagate(False)

n2 = Label(c2, text=str(c_cnt), font=("Arial Black", 32, "bold"), fg="#27ae60", bg="white")
n2.place(relx=0.5, rely=0.3, anchor="center")

t2 = Label(c2, text="Reviews Completed", font=("Arial Black", 12), fg="gray", bg="white")
t2.place(relx=0.5, rely=0.7, anchor="center")

table = Frame(main, bg="white", bd=1, relief=SOLID)
table.place(x=50, y=220, relwidth=0.85, height=350)

lbl_recent = Label(table, text="Recent Working Papers", font=("Arial Black", 14), bg="white", fg="#2c3e50")
lbl_recent.pack(pady=10, anchor="w", padx=20)

head = Frame(table, bg="#2c3e50")
head.pack(fill=X, padx=20)

Label(head, text="Filename", font=("Arial Black", 10), bg="#2c3e50", fg="white", width=35, anchor="w").pack(side=LEFT, padx=5, pady=5)
Label(head, text="Status", font=("Arial Black", 10), bg="#2c3e50", fg="white", width=12, anchor="center").pack(side=LEFT, padx=5, pady=5)
Label(head, text="Date", font=("Arial Black", 10), bg="#2c3e50", fg="white", width=18, anchor="center").pack(side=LEFT, padx=5, pady=5)

if recent:
    for i, (name, status, date) in enumerate(recent):
        bg = "#f9f9f9" if i % 2 == 0 else "white"
        row = Frame(table, bg=bg)
        row.pack(fill=X, padx=20)

        Label(row, text=name, font=("Arial", 10), bg=bg, fg="#2c3e50", width=35, anchor="w").pack(side=LEFT, padx=5, pady=4)

        fg = "#27ae60" if status == "ACCEPTED" else "#e74c3c" if status == "REJECTED" else "#e67e22"
        Label(row, text=status, font=("Arial", 10, "bold"), bg=bg, fg=fg, width=12, anchor="center").pack(side=LEFT, padx=5, pady=4)

        dt = date.strftime("%Y-%m-%d %H:%M") if date else ""
        Label(row, text=dt, font=("Arial", 10), bg=bg, fg="#7f8c8d", width=18, anchor="center").pack(side=LEFT, padx=5, pady=4)
else:
    Label(table, text="No working papers uploaded yet.", font=("Arial", 11), bg="white", fg="#bdc3c7").pack(pady=30)

window.mainloop()