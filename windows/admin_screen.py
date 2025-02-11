import customtkinter as ctk
import subprocess
import customtkinter
from tkinter import *
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
# Function definitions external scripts run karane ke liye
def run_subjects():
    subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\subjects.py'], shell=True)

def run_faculty():
    subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\faculty.py'], shell=True)

def run_students():
    subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\student.py'], shell=True)

def run_scheduler():
    subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\scheduler.py'], shell=True)

def run_timetable_students():
    subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\timetable_stud.py'], shell=True)

def run_timetable_faculty():
    subprocess.Popen(['python', r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\windows\timetable_fac.py'], shell=True)

# CustomTkinter main window setup ke liye
ad = ctk.CTk()
ad.geometry('600x360')
ad.title('Administrator')
image = Image.open(r'C:\Users\MOHD SUHAIL\Downloads\bg4.jpg')
my_image = ImageTk.PhotoImage(image)
l21 = Label(image=my_image)
l21.place(relheight=1, relwidth=1)

# font ke liye
stylish_font_large = ('Helvetica Neue', 22, 'bold')
stylish_font_medium = ('Helvetica Neue', 16, 'italic')
stylish_font_small = ('Helvetica Neue', 12)

# Main Frame sare content ke liye
main_frame = ctk.CTkFrame(master=ad, corner_radius=20, width=450, height=450)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
title_label = ctk.CTkLabel(
    master=main_frame,
    text='A D M I N I S T R A T O R',
    font=stylish_font_large,
)
title_label.pack(pady=10)

subtitle_label = ctk.CTkLabel(
    master=main_frame,
    text='You are the Administrator',
    font=stylish_font_medium
)
subtitle_label.pack(pady=9)

# Modify Frame
modify_frame = ctk.CTkFrame(master=main_frame, corner_radius=10)
modify_frame.pack(pady=10, padx=10, side="left", anchor="n")

modify_label = ctk.CTkLabel(master=modify_frame, text="Modify", font=stylish_font_medium)
modify_label.pack(pady=5)

ctk.CTkButton(
    master=modify_frame,
    text='Subjects',
    command=run_subjects,
    font=stylish_font_small
).pack(pady=5)

ctk.CTkButton(
    master=modify_frame,
    text='Faculties',
    command=run_faculty,
    font=stylish_font_small
).pack(pady=5)

ctk.CTkButton(
    master=modify_frame,
    text='Students',
    command=run_students,
    font=stylish_font_small
).pack(pady=5)

# Timetable Frame
tt_frame = ctk.CTkFrame(master=main_frame, corner_radius=10)
tt_frame.pack(pady=10, padx=10, side="right", anchor="n")

tt_label = ctk.CTkLabel(master=tt_frame, text="Timetable", font=stylish_font_medium)
tt_label.pack(pady=5)

ctk.CTkButton(
    master=tt_frame,
    text='Schedule Periods',
    command=run_scheduler,
    font=stylish_font_small
).pack(pady=5)

ctk.CTkButton(
    master=tt_frame,
    text='View Section-Wise',
    command=run_timetable_students,
    font=stylish_font_small
).pack(pady=5)

ctk.CTkButton(
    master=tt_frame,
    text='View Faculty-wise',
    command=run_timetable_faculty,
    font=stylish_font_small
).pack(pady=5)

# Quit Button
ctk.CTkButton(
    master=main_frame,
    text='Quit',
    command=ad.destroy,
    fg_color='red',
    font=stylish_font_small
).pack(pady=15)

ad.mainloop()
