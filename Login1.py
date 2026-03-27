import tkinter as tk
from PIL import Image, ImageTk


window = tk.Tk()
window.title("AuditPro - Login")
window.geometry("950x533")
window.resizable(True,True)

bg_img = Image.open("img1.jpg")
bg_photo = ImageTk.PhotoImage(bg_img)
window.resizable(True,True)

image_label = tk.Label(window, image=bg_photo)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

title = tk.Label(window, text="AuditPro", font=("Arial Black", 24, "bold"), fg="#2c3e50")
title.place(relx=0.5, y=80, anchor="n")

subtitle = tk.Label(window, text="An interface for audit management", font=("Arial Black", 12), fg="#7f8c8d")
subtitle.place(relx=0.5, y=120, anchor="n")

form = tk.LabelFrame(window, text="Login", font=("Arial Black", 12), width=400, height=300)
form.place(relx=0.5, y=170, anchor="n")

tk.Label(form, text="Username:", font=("Arial Black", 11)).place(x=50, y=60)
username_entry = tk.Entry(form, width=25)
username_entry.place(x=160, y=60)

tk.Label(form, text="Password:", font=("Arial Black", 11)).place(x=50, y=110)
password_entry = tk.Entry(form, width=25, show="*")
password_entry.place(x=160, y=110)

window.mainloop()