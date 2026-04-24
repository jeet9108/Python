from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))

def get_state():
    if window.state() == 'zoomed':
        return 'zoomed'
    return window.geometry()

def back():
    st = get_state()
    window.destroy()
    os.system(f'python "{os.path.join(path, "dashboard.py")}" --window-state "{st}"')

def open_db():
    webbrowser.open("http://localhost/phpmyadmin/index.php?route=/database/structure&db=ca")

window = Tk()
window.title("AuditPro - Database Manager")
window.geometry("1000x700")

if '--window-state' in sys.argv:
    idx = sys.argv.index('--window-state')
    if idx + 1 < len(sys.argv):
        st = sys.argv[idx + 1]
        if st == 'zoomed':
            window.state('zoomed')
        else:
            window.geometry(st)

side = Frame(window, bg="#2c3e50", width=250)
side.pack(side=LEFT, fill=Y)
side.pack_propagate(False)

try:
    log_path = os.path.join(path, "..", "..", "Images", "img3.jpeg")
    log_img = Image.open(log_path).resize((150, 100))
    log_photo = ImageTk.PhotoImage(log_img)
    logo = Label(side, image=log_photo, bg="#2c3e50")
    logo.image = log_photo
except:
    logo = Label(side, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
logo.pack(pady=20)


role = Label(side, text="Role: Admin", bg="#2c3e50", fg="#bdc3c7", font=("Arial Black", 10))
role.pack(pady=10)

btn1 = Button(side, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=back)
btn1.pack(pady=5)

main = Frame(window, bg="#ecf0f1")
main.pack(side=LEFT, fill=BOTH, expand=True)

title = Label(main, text="Database Manager", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
title.place(x=50, y=40)

box = Frame(main, bg="white", bd=2, relief=GROOVE)
box.place(x=50, y=100, width=600, height=300)

info = Label(box, text="phpMyAdmin Database", font=("Arial Black", 14), bg="white", fg="#2c3e50")
info.place(relx=0.5, y=50, anchor=CENTER)

icon = Label(box, font=("Arial", 48), bg="white", fg="#f39c12")
icon.place(relx=0.5, y=120, anchor=CENTER)

btn2 = Button(box, text="Open phpMyAdmin", bg="#f39c12", fg="white", font=("Arial Black", 14, "bold"), width=30, pady=5, command=open_db)
btn2.place(relx=0.5, y=200, anchor=CENTER)

window.mainloop()

