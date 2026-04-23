from tkinter import *
from PIL import Image, ImageTk
import os
import sys

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

def get_window_state():
    """Get the current window state to pass back to the dashboard."""
    if window.state() == 'zoomed':
        return 'zoomed'
    else:
        return window.geometry()

def go_back():
    state = get_window_state()
    window.destroy()
    os.system(f'python "{os.path.join(script_dir, "dashboard.py")}" --window-state "{state}"')

window = Tk()
window.title("AuditPro - Help (Accounting Standards)")
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

lbl_title = Label(content_area, text="Accounting Standards Reference", font=("Arial Black", 20), bg="#e1f5fe", fg="#2c3e50")
lbl_title.pack(pady=20)

# Frame for the Image (Scrollable if needed)
image_frame = Frame(content_area, bg="white", bd=2, relief=GROOVE)
image_frame.pack(padx=30, pady=10, fill=BOTH, expand=True)

# Add a Canvas and Scrollbar for the image
canvas = Canvas(image_frame, bg="white")
scrollbar = Scrollbar(image_frame, orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Load and Display the Image
try:
    img_path = os.path.join(script_dir, "..", "..", "Images", "as_standards.png")
    help_img = Image.open(img_path)
    
    # Resize image to fit width while maintaining aspect ratio
    original_width, original_height = help_img.size
    display_width = 700
    display_height = int((display_width / original_width) * original_height)
    
    help_img_resized = help_img.resize((display_width, display_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(help_img_resized)
    
    img_label = Label(scrollable_frame, image=photo, bg="white")
    img_label.image = photo  # Keep reference
    img_label.pack()
except Exception as e:
    Label(scrollable_frame, text=f"Could not load 'as_standards.png'.\nPlease ensure the image is in the Images folder.", 
          font=("Arial", 12), bg="white", fg="red").pack(pady=100)

window.mainloop()
