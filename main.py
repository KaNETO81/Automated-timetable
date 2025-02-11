import tkinter as tk
from tkinter import messagebox
import sqlite3
import customtkinter
import subprocess
import sys
from PIL import Image, ImageTk

# Adding the path for timetable modules
sys.path.insert(0, r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows')
import timetable_stud
import timetable_fac

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")  # Themes: blue, dark-blue, or green

# Main Application
app = customtkinter.CTk()
app.geometry("600x600")
app.title("LOGIN")

# Set Background Image
image = Image.open(r'C:\Users\MOHD SUHAIL\Downloads\bg.jpg')
my_image = ImageTk.PhotoImage(image)
lbl = tk.Label(image=my_image)
lbl.place(relheight=1, relwidth=1)


def challenge():
    conn = sqlite3.connect(r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db')
    user = str(combo1.get())

    if user == "Student":
        cursor = conn.execute(
            "SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID=?", 
            (id_entry.get(),)
        ).fetchall()
        if len(cursor) == 0:
            messagebox.showwarning('Bad ID', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Incorrect Password', 'Incorrect Password!')
        else:
            # nw = tk.Tk()
            # tk.Label(
            #     nw,
            #     text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tRoll No.: {cursor[0][3]}',
            #     font=('Consolas', 12, 'italic'),
            # ).pack()
            if app.winfo_exists():
                app.destroy()
            subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\timetable_stud.py'], shell=True)

    elif user == "Faculty":
        cursor = conn.execute(
            "SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID=?", 
            (id_entry.get(),)
        ).fetchall()
        if len(cursor) == 0:
            messagebox.showwarning('Bad ID', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Incorrect Password', 'Incorrect Password!')
        else:
            if app.winfo_exists():
                app.destroy()
            subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\timetable_fac.py'], shell=True)

    elif user == "Admin":
        cursor = conn.execute(
            "SELECT PASSW, NAME, EMAIL FROM ADMIN WHERE AID=?", 
            (id_entry.get(),)
        ).fetchall()
        if len(cursor) == 0:
            messagebox.showwarning('Bad ID', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Incorrect Password', 'Incorrect Password!')
        else:
            if app.winfo_exists():
                app.destroy()
            subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\admin_screen.py'], shell=True)


# Main Frame
frame = customtkinter.CTkFrame(master=app, width=320, height=380, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title Label
l2 = customtkinter.CTkLabel(master=frame, text="LOG IN", font=("Century Gothic", 20))
l2.place(x=18, y=20)

# Dropdown Menu (User Selection)
combo1 = customtkinter.CTkOptionMenu(master=frame, values=["Student", "Faculty", "Admin"])
combo1.place(x=50, y=70)
combo1.set("Student")

# ID Entry
id_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="USERNAME ID")
id_entry.place(x=50, y=120)

# Password Entry
passw_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="PASSWORD", show="*")
passw_entry.place(x=50, y=180)

# Login Button
button1 = customtkinter.CTkButton(
    master=frame, width=220, text="LOGIN", corner_radius=6, command=challenge
)
button1.place(x=50, y=235)

app.mainloop()

