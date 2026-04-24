from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import os
import sys
import shutil
import mysql.connector

path = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.abspath(os.path.join(path, "..", "..", "working_papers_storage"))
if not os.path.exists(STORE):
    os.makedirs(STORE)

def connect():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="ca"
    )

def get_state():
    if window.state() == 'zoomed':
        return 'zoomed'
    return window.geometry()

def back():
    st = get_state()
    window.destroy()
    os.system(f'python "{os.path.join(path, "dashboard.py")}" --window-state "{st}"')

def load_data():
    box_list.delete(0, END)
    try:
        db = connect()
        cur = db.cursor()
        cur.execute("SELECT id, filename, status, filepath FROM working_papers ORDER BY created_at DESC")
        for row in cur.fetchall():
            db_id, name, status, fp = row
            txt = f"[{status}] {name}"
            box_list.insert(END, txt)
            idx = box_list.size() - 1
            if status == "ACCEPTED": box_list.itemconfig(idx, {'fg': 'green'})
            elif status == "REJECTED": box_list.itemconfig(idx, {'fg': 'red'})
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"Load failed: {e}")

def get_name(txt):
    for p in ["[PENDING] ", "[ACCEPTED] ", "[REJECTED] "]:
        if txt.startswith(p): return txt[len(p):]
    return txt

def add():
    fp = filedialog.askopenfilename(title="Select File")
    if fp:
        name = os.path.basename(fp)
        dst = os.path.join(STORE, name)
        base, ext = os.path.splitext(name)
        c = 1
        while os.path.exists(dst):
            name = f"{base}_{c}{ext}"
            dst = os.path.join(STORE, name)
            c += 1
        shutil.copy2(fp, dst)
        try:
            db = connect()
            cur = db.cursor()
            cur.execute("INSERT INTO working_papers (filename, status, filepath) VALUES (%s, %s, %s)", (name, "PENDING", dst))
            db.commit()
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")
            return
        load_data()

def open_file(e):
    sel = box_list.curselection()
    if not sel: return
    name = get_name(box_list.get(sel[0]))
    fp = os.path.join(STORE, name)
    if os.path.exists(fp): os.startfile(fp)
    else: messagebox.showerror("Error", "File not found")

def delete():
    sel = box_list.curselection()
    if sel:
        name = get_name(box_list.get(sel[0]))
        if not messagebox.askyesno("Confirm", f"Remove '{name}'?"): return
        try:
            db = connect()
            cur = db.cursor()
            cur.execute("DELETE FROM working_papers WHERE filename = %s", (name,))
            db.commit()
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")
            return
        fp = os.path.join(STORE, name)
        if os.path.exists(fp): os.remove(fp)
        load_data()
    else: messagebox.showwarning("Warning", "Select a paper")

def update_status(st):
    sel = box_list.curselection()
    if sel:
        name = get_name(box_list.get(sel[0]))
        try:
            db = connect()
            cur = db.cursor()
            cur.execute("UPDATE working_papers SET status = %s WHERE filename = %s", (st, name))
            db.commit()
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")
            return
        load_data()
    else: messagebox.showwarning("Warning", "Select a paper")

window = Tk()
window.title("AuditPro - Working Papers")
window.geometry("1000x700")

if '--window-state' in sys.argv:
    idx = sys.argv.index('--window-state')
    if idx + 1 < len(sys.argv):
        st = sys.argv[idx + 1]
        if st == 'zoomed': window.state('zoomed')
        else: window.geometry(st)

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


role = Label(side, text="Role: CA_Yogesh_Shah", bg="#2c3e50", fg="#bdc3c7", font=("Arial Black", 10))
role.pack(pady=10)

btn_back = Button(side, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=back)
btn_back.pack(pady=5)

main = Frame(window, bg="#ecf0f1")
main.pack(side=LEFT, fill=BOTH, expand=True)

title = Label(main, text="Working Papers Module", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
title.place(x=50, y=40)

hint = Label(main, text="Double-click a file to open it.", font=("Arial", 10), bg="#ecf0f1", fg="#7f8c8d")
hint.place(x=60, y=80)

box = Frame(main, bg="white", bd=2, relief=GROOVE)
box.place(x=50, y=100, width=650, height=450)

Label(box, text="Attached Working Papers:", font=("Arial Black", 12), bg="white").pack(pady=10, anchor="w", padx=20)

box_list = Listbox(box, font=("Arial", 11), width=65, height=15)
box_list.pack(pady=5, padx=20)
box_list.bind("<Double-Button-1>", open_file)

btns = Frame(box, bg="white")
btns.pack(pady=20, fill=X, padx=20)

Button(btns, text="Attach", bg="#3498db", fg="white", font=("Arial Black", 10), width=10, command=add).pack(side=LEFT, padx=5)
Button(btns, text="Remove", bg="#e74c3c", fg="white", font=("Arial Black", 10), width=10, command=delete).pack(side=LEFT, padx=5)
Button(btns, text="Reject", bg="#e67e22", fg="white", font=("Arial Black", 10), width=10, command=lambda: update_status("REJECTED")).pack(side=RIGHT, padx=5)
Button(btns, text="Accept", bg="#27ae60", fg="white", font=("Arial Black", 10), width=10, command=lambda: update_status("ACCEPTED")).pack(side=RIGHT, padx=5)

load_data()
window.mainloop()

