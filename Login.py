from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector

def open_dashboard():
    window.destroy()
    os.system('python dashboard.py')

def check_login():
    user = username_entry.get()
    passw = password_entry.get()
    logintodb(user, passw)

def logintodb(user, passw):
    con = mysql.connector.connect(
              host="localhost",
              user="root",
              password="",
              database="ca"
              )
    cursor = con.cursor()          
    # A Table in the database
    savequery = "select * from login"      
    try:
        cursor.execute(savequery)
        myresult = cursor.fetchall()
        status=False  
        # Printing the result of the
        # query
        for x in myresult:
            if x[0]==user and x[1]==passw :
                status=True
                break;
        if status:     
            message_label.config(text="Login Successful", fg="green")
            window.after(1000, open_dashboard)
        else:
            message_label.config(text="Wrong Username or Password", fg="red")  
    except:
        con.rollback()
        print("Error occured")

def clear_data():
    username_entry.delete(0, END)
    password_entry.delete(0, END)

window = Tk()
window.title("AuditPro - Login")
window.geometry("950x533")

bg_img = Image.open("img1.jpg")
bg_photo = ImageTk.PhotoImage(bg_img.resize((950, 533)))

image_label = Label(window, image=bg_photo)
image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

def resize_image(event):
    global bg_photo
    if event.width > 1 and event.height > 1:
        resized = bg_img.resize((event.width, event.height))
        bg_photo = ImageTk.PhotoImage(resized)
        image_label.config(image=bg_photo)

window.bind("<Configure>", resize_image)

title = Label(window, text="AuditPro", font=("Arial Black", 24, "bold"), fg="#2c3e50", bg="white")
title.place(relx=0.5, y=80, anchor="center")

subtitle = Label(window, text="An interface for audit management", font=("Arial Black", 12), fg="#7f8c8d", bg="white")
subtitle.place(relx=0.5, y=120, anchor="center")

form = Frame(window, bg="white", width=400, height=300, bd=2, relief=GROOVE)
form.place(relx=0.5, rely=0.5, anchor="center")
form.pack_propagate(False)

form_title = Label(form, text="Login", font=("Arial Black", 14, "bold"), bg="white")
form_title.place(relx=0.5, y=20, anchor="center")

lbl_user = Label(form, text="Username:", font=("Arial Black", 11), bg="white")
lbl_user.place(x=50, y=80)
username_entry = Entry(form, width=25)
username_entry.place(x=160, y=80)

lbl_pass = Label(form, text="Password:", font=("Arial Black", 11), bg="white")
lbl_pass.place(x=50, y=130)
password_entry = Entry(form, width=25, show="*")
password_entry.place(x=160, y=130)

login_button = Button(form, text="Login", bg="#3498db", fg="white", font=("Arial Black", 11, "bold"), width=12, command=check_login)
login_button.place(x=60, y=200)

clear_button = Button(form, text="Clear", bg="#e74c3c", fg="white", font=("Arial Black", 11, "bold"), width=12, command=clear_data)
clear_button.place(x=200, y=200)

message_label = Label(form, text="", font=("Arial", 10), bg="white")
message_label.place(relx=0.5, y=250, anchor="center")

window.mainloop()