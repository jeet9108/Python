from tkinter import *
from tkinter import filedialog, messagebox
import os
import sys
import shutil
import mysql.connector

# Directory to store copies of taxing standards and guidelines
script_dir = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.abspath(os.path.join(script_dir, "..", "..", "help_documents_storage"))
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def get_db_connection():
    """Get a MySQL database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ca"
    )

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

def load_documents_from_db():
    """Load help documents from the database and display in the listbox."""
    docs_listbox.delete(0, END)
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT filename FROM help_documents ORDER BY created_at DESC")
        rows = cursor.fetchall()
        for row in rows:
            docs_listbox.insert(END, row[0])
        con.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not load documents: {e}")

def attach_document():
    filepath = filedialog.askopenfilename(title="Select Standard/Guideline Document")
    if filepath:
        filename = os.path.basename(filepath)
        dest_path = os.path.join(STORAGE_DIR, filename)

        # Handle duplicate filenames
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            filename = f"{base}_{counter}{ext}"
            dest_path = os.path.join(STORAGE_DIR, filename)
            counter += 1

        # Copy the file to storage directory
        shutil.copy2(filepath, dest_path)

        # Insert into database
        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO help_documents (filename, filepath) VALUES (%s, %s)",
                (filename, dest_path)
            )
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save to database: {e}")
            return

        # Refresh the listbox
        load_documents_from_db()

def open_document(event=None):
    """Open the selected document."""
    selected = docs_listbox.curselection()
    if not selected:
        return
    filename = docs_listbox.get(selected[0])
    stored_path = os.path.join(STORAGE_DIR, filename)

    if os.path.exists(stored_path):
        os.startfile(stored_path)
    else:
        messagebox.showerror("Error", f"File not found:\n{stored_path}")

def remove_document():
    selected = docs_listbox.curselection()
    if selected:
        filename = docs_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm", f"Remove '{filename}'?")
        if not confirm:
            return

        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute("DELETE FROM help_documents WHERE filename = %s", (filename,))
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not delete from database: {e}")
            return

        stored_path = os.path.join(STORAGE_DIR, filename)
        if os.path.exists(stored_path):
            os.remove(stored_path)

        load_documents_from_db()

window = Tk()
window.title("AuditPro - Help & Guidelines")
window.geometry("1000x700")

# Restore window state
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

btn_back = Button(sidebar, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=go_back)
btn_back.pack(pady=5)

# Content Area
content_area = Frame(window, bg="#e1f5fe")
content_area.pack(side=LEFT, fill=BOTH, expand=True)

lbl_title = Label(content_area, text="Help & Taxing Standards", font=("Arial Black", 24), bg="#e1f5fe", fg="#2c3e50")
lbl_title.place(x=50, y=40)

lbl_desc = Label(content_area, text="Upload and view professional guidelines and taxing standards here.", font=("Arial", 12), bg="#e1f5fe", fg="#34495e")
lbl_desc.place(x=50, y=90)

form_frame = Frame(content_area, bg="white", bd=2, relief=GROOVE)
form_frame.place(x=50, y=130, width=700, height=450)

docs_listbox = Listbox(form_frame, font=("Arial", 12), width=70, height=15)
docs_listbox.pack(pady=20, padx=20)
docs_listbox.bind("<Double-Button-1>", open_document)

btn_frame = Frame(form_frame, bg="white")
btn_frame.pack(pady=10, fill=X, padx=20)

btn_attach = Button(btn_frame, text="Upload Guideline", bg="#3498db", fg="white", font=("Arial Black", 10), command=attach_document)
btn_attach.pack(side=LEFT, padx=5)

btn_open = Button(btn_frame, text="Open Document", bg="#27ae60", fg="white", font=("Arial Black", 10), command=open_document)
btn_open.pack(side=LEFT, padx=5)

btn_remove = Button(btn_frame, text="Remove", bg="#e74c3c", fg="white", font=("Arial Black", 10), command=remove_document)
btn_remove.pack(side=RIGHT, padx=5)

load_documents_from_db()
window.mainloop()
