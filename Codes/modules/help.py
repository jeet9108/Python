from tkinter import *
from PIL import Image, ImageTk
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

window = Tk()
window.title("AuditPro - Help")
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

logo = Label(side, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
logo.pack(pady=30)

btn1 = Button(side, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=back)
btn1.pack(pady=5)

main = Frame(window, bg="#e1f5fe")
main.pack(side=LEFT, fill=BOTH, expand=True)

title = Label(main, text="Accounting Standards Reference", font=("Arial Black", 20), bg="#e1f5fe", fg="#2c3e50")
title.pack(pady=20)

box = Frame(main, bg="white", bd=2, relief=GROOVE)
box.pack(padx=30, pady=10, fill=BOTH, expand=True)

canv = Canvas(box, bg="white")
scrol = Scrollbar(box, orient=VERTICAL, command=canv.yview)
view = Frame(canv, bg="white")

view.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
canv.create_window((0, 0), window=view, anchor="nw")
canv.configure(yscrollcommand=scrol.set)

canv.pack(side=LEFT, fill=BOTH, expand=True)
scrol.pack(side=RIGHT, fill=Y)

try:
    img_path = os.path.join(path, "..", "..", "Images", "img4.png")
    img = Image.open(img_path)
    w, h = img.size
    nw = 1200
    nh = int((nw / w) * h)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    lbl = Label(view, image=photo, bg="white")
    lbl.image = photo
    lbl.pack()
except:
    Label(view, text="Error loading image.", font=("Arial", 12), bg="white", fg="red").pack(pady=400)

window.mainloop()

