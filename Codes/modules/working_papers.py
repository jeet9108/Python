from tkinter import *
from tkinter import filedialog, messagebox
import os
import sys
import shutil
import mysql.connector

# Directory to store copies of attached working papers
script_dir = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.abspath(os.path.join(script_dir, "..", "..", "working_papers_storage"))
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

def load_papers_from_db():
    """Load working papers from the database and display in the listbox."""
    papers_listbox.delete(0, END)
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT id, filename, status, filepath FROM working_papers ORDER BY created_at DESC")
        rows = cursor.fetchall()
        for row in rows:
            db_id, filename, status, filepath = row
            display_text = f"[{status}] {filename}"
            papers_listbox.insert(END, display_text)
            # Set color based on status
            idx = papers_listbox.size() - 1
            if status == "ACCEPTED":
                papers_listbox.itemconfig(idx, {'fg': 'green'})
            elif status == "REJECTED":
                papers_listbox.itemconfig(idx, {'fg': 'red'})
        con.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not load papers: {e}")

def get_filename_from_text(text):
    """Extract filename from display text like '[PENDING] filename.csv'."""
    for prefix in ["[PENDING] ", "[ACCEPTED] ", "[REJECTED] "]:
        if text.startswith(prefix):
            return text[len(prefix):]
    return text

def attach_paper():
    filepath = filedialog.askopenfilename(title="Select Working Paper")
    if filepath:
        filename = os.path.basename(filepath)
        dest_path = os.path.join(STORAGE_DIR, filename)

        # Handle duplicate filenames by appending a number
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
                "INSERT INTO working_papers (filename, status, filepath) VALUES (%s, %s, %s)",
                (filename, "PENDING", dest_path)
            )
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save to database: {e}")
            return

        # Refresh the listbox from DB
        load_papers_from_db()

def open_paper(event):
    """Open the selected working paper with the default system application."""
    selected = papers_listbox.curselection()
    if not selected:
        return
    idx = selected[0]
    text = papers_listbox.get(idx)
    filename = get_filename_from_text(text)
    stored_path = os.path.join(STORAGE_DIR, filename)

    if os.path.exists(stored_path):
        os.startfile(stored_path)
    else:
        messagebox.showerror("Error", f"File not found:\n{stored_path}")

def remove_paper():
    selected = papers_listbox.curselection()
    if selected:
        idx = selected[0]
        text = papers_listbox.get(idx)
        filename = get_filename_from_text(text)

        confirm = messagebox.askyesno("Confirm", f"Remove '{filename}' from working papers?\nThis will delete the stored copy.")
        if not confirm:
            return

        # Delete from database
        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute("DELETE FROM working_papers WHERE filename = %s", (filename,))
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not delete from database: {e}")
            return

        # Delete stored file
        stored_path = os.path.join(STORAGE_DIR, filename)
        if os.path.exists(stored_path):
            os.remove(stored_path)

        # Refresh listbox
        load_papers_from_db()
    else:
        messagebox.showwarning("Warning", "Please select a paper to remove")

def accept_paper():
    selected = papers_listbox.curselection()
    if selected:
        idx = selected[0]
        text = papers_listbox.get(idx)
        filename = get_filename_from_text(text)

        # Update status in database
        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute("UPDATE working_papers SET status = 'ACCEPTED' WHERE filename = %s", (filename,))
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update status: {e}")
            return

        # Refresh listbox
        load_papers_from_db()
    else:
        messagebox.showwarning("Warning", "Please select a paper to accept")

def reject_paper():
    selected = papers_listbox.curselection()
    if selected:
        idx = selected[0]
        text = papers_listbox.get(idx)
        filename = get_filename_from_text(text)

        # Update status in database
        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute("UPDATE working_papers SET status = 'REJECTED' WHERE filename = %s", (filename,))
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update status: {e}")
            return

        # Refresh listbox
        load_papers_from_db()
    else:
        messagebox.showwarning("Warning", "Please select a paper to reject")

window = Tk()
window.title("AuditPro - Working Papers")
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

lbl_role = Label(sidebar, text="Role: CA_Yogesh_Shah", bg="#2c3e50", fg="#bdc3c7", font=("Arial Black", 10))
lbl_role.pack(pady=10)

btn_back = Button(sidebar, text="Back to Dashboard", bg="white", font=("Arial Black", 12), width=20, command=go_back)
btn_back.pack(pady=5)

# Content
content_area = Frame(window, bg="#ecf0f1")
content_area.pack(side=LEFT, fill=BOTH, expand=True)

lbl_title = Label(content_area, text="Working Papers Module", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
lbl_title.place(x=50, y=40)

# Hint label
lbl_hint = Label(content_area, text="Double-click a file to open it. Changes saved in the app will be auto-saved.",
                 font=("Arial", 10), bg="#ecf0f1", fg="#7f8c8d")
lbl_hint.place(x=50, y=75)

# Main frame for working papers view
form_frame = Frame(content_area, bg="white", bd=2, relief=GROOVE)
form_frame.place(x=50, y=100, width=650, height=450)

lbl_list = Label(form_frame, text="Attached Working Papers:", font=("Arial Black", 12), bg="white")
lbl_list.pack(pady=10, anchor="w", padx=20)

papers_listbox = Listbox(form_frame, font=("Arial", 11), width=65, height=15)
papers_listbox.pack(pady=5, padx=20)

# Bind double-click to open the file
papers_listbox.bind("<Double-Button-1>", open_paper)

btn_frame = Frame(form_frame, bg="white")
btn_frame.pack(pady=20, fill=X, padx=20)

btn_attach = Button(btn_frame, text="Attach", bg="#3498db", fg="white", font=("Arial Black", 10), width=10, command=attach_paper)
btn_attach.pack(side=LEFT, padx=5)

btn_remove = Button(btn_frame, text="Remove", bg="#e74c3c", fg="white", font=("Arial Black", 10), width=10, command=remove_paper)
btn_remove.pack(side=LEFT, padx=5)

btn_reject = Button(btn_frame, text="Reject", bg="#e67e22", fg="white", font=("Arial Black", 10), width=10, command=reject_paper)
btn_reject.pack(side=RIGHT, padx=5)

btn_accept = Button(btn_frame, text="Accept", bg="#27ae60", fg="white", font=("Arial Black", 10), width=10, command=accept_paper)
btn_accept.pack(side=RIGHT, padx=5)

# Load papers from database on startup
load_papers_from_db()

window.mainloop()
