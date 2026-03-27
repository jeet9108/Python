from tkinter import *
def open_dashboard():
    window.destroy()
    os.system('python dashboard.py')

def logout_to_login:
    user = username_entry.get()
    passw = password_entry.get()
    logintodb(user, passw)

window = Tk()
window.title("AuditPro")
window.geometry("1000x700")

sidebar = Frame(window, bg="#2c3e50", width=250)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

lbl_logo = Label(sidebar, text="AuditPro", bg="#2c3e50", fg="white", font=("Arial Black", 20, "bold"))
lbl_logo.pack(pady=30)

btn_dash = Button(sidebar, text="Dashboard", bg="white", font=("Arial Black", 12), width=20)
btn_dash.pack(pady=5)

btn_wp = Button(sidebar, text="Working Papers", bg="white", font=("Arial Black", 12), width=20)
btn_wp.pack(pady=5)

btn_user_mgmt = Button(sidebar, text="User Management", bg="white", font=("Arial Black", 12), width=20)
btn_user_mgmt.pack(pady=5)

btn_db = Button(sidebar, text="Database Manager", bg="white", font=("Arial Black", 12), width=20)
btn_db.pack(pady=5)

btn_logout = Button(sidebar, text="Logout", bg="#c0392b", fg="white", font=("Arial Black", 10, "bold"), width=20, command = logout_to_login)
btn_logout.pack(side=BOTTOM, pady=20)

content_area = Frame(window, bg="#ecf0f1")
content_area.pack(side=LEFT, fill=BOTH, expand=True)

lbl_welcome = Label(content_area, text="Welcome back, CA Yogesh Shah", font=("Arial Black", 24), bg="#ecf0f1", fg="#2c3e50")
lbl_welcome.place(x=50, y=40)

cards_frame = Frame(content_area, bg="#ecf0f1")
cards_frame.place(relx=0.5, rely=0.3, anchor="center")

card1 = Frame(cards_frame, bg="white", width=250, height=120, bd=1, relief=SOLID)
card1.pack(side=LEFT, padx=50)
card1.pack_propagate(False)

lbl_num1 = Label(card1, text="0", font=("Arial Black", 32, "bold"), fg="#e67e22", bg="white")
lbl_num1.place(relx=0.5, rely=0.3, anchor="center")

lbl_txt1 = Label(card1, text="Reviews Pending", font=("Arial Black", 12), fg="gray", bg="white")
lbl_txt1.place(relx=0.5, rely=0.7, anchor="center")

card2 = Frame(cards_frame, bg="white", width=250, height=120, bd=1, relief=SOLID)
card2.pack(side=LEFT, padx=50)
card2.pack_propagate(False)

lbl_num2 = Label(card2, text="0", font=("Arial Black", 32, "bold"), fg="#27ae60", bg="white")
lbl_num2.place(relx=0.5, rely=0.3, anchor="center")

lbl_txt2 = Label(card2, text="Reviews Completed", font=("Arial Black", 12), fg="gray", bg="white")
lbl_txt2.place(relx=0.5, rely=0.7, anchor="center")

window.mainloop()