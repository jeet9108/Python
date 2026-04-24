from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import mysql.connector

def get_state():
    if window.state() == 'zoomed': return 'zoomed'
    return window.geometry()

def open_dash():
    st = get_state()
    window.destroy()
    path = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python "{os.path.join(path, "dashboard.py")}" --window-state "{st}"')

def check():
    u, p = e1.get(), e2.get()
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="", database="ca")
        cur = db.cursor()
        cur.execute("SELECT * FROM login")
        ok = False
        for r in cur.fetchall():
            if r[0] == u and r[1] == p:
                ok = True
                break
        if ok:
            msg.config(text="Login Successful", fg="green")
            window.after(1000, open_dash)
        else:
            msg.config(text="Wrong Username or Password", fg="red")
    except: msg.config(text="Database Error", fg="red")

def clear():
    e1.delete(0, END)
    e2.delete(0, END)

window = Tk()
window.title("AuditPro - Login")
window.geometry("950x533")

if '--window-state' in sys.argv:
    idx = sys.argv.index('--window-state')
    if idx + 1 < len(sys.argv):
        st = sys.argv[idx + 1]
        if st == 'zoomed': window.state('zoomed')
        else: window.geometry(st)

path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.abspath(os.path.join(path, "..", "..", "Images", "img1.jpg"))
img_orig = Image.open(img_path)
bg_img = ImageTk.PhotoImage(img_orig.resize((950, 533)))

bg_lbl = Label(window, image=bg_img)
bg_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

def resize(e):
    global bg_img
    if e.width > 1 and e.height > 1:
        bg_img = ImageTk.PhotoImage(img_orig.resize((e.width, e.height)))
        bg_lbl.config(image=bg_img)

window.bind("<Configure>", resize)

Label(window, text="AuditPro", font=("Arial Black", 24, "bold"), fg="#2c3e50", bg="white").place(relx=0.5, y=70, anchor="center")
Label(window, text="An interface for audit management", font=("Arial Black", 12), fg="#7f8c8d", bg="white").place(relx=0.5, y=100, anchor="center")

box = Frame(window, bg="white", width=400, height=300, bd=2, relief=GROOVE)
box.place(relx=0.5, rely=0.5, anchor="center")
box.pack_propagate(False)

Label(box, text="Login", font=("Arial Black", 14, "bold"), bg="white").place(relx=0.5, y=20, anchor="center")
Label(box, text="Username:", font=("Arial Black", 11), bg="white").place(x=50, y=80)
e1 = Entry(box, width=25)
e1.place(x=160, y=80)

Label(box, text="Password:", font=("Arial Black", 11), bg="white").place(x=50, y=130)
e2 = Entry(box, width=25, show="*")
e2.place(x=160, y=130)

Button(box, text="Login", bg="#3498db", fg="white", font=("Arial Black", 11, "bold"), width=12, command=check).place(x=60, y=200)
Button(box, text="Clear", bg="#e74c3c", fg="white", font=("Arial Black", 11, "bold"), width=12, command=clear).place(x=200, y=200)

msg = Label(box, text="", font=("Arial", 10), bg="white")
msg.place(relx=0.5, y=250, anchor="center")

window.mainloop()