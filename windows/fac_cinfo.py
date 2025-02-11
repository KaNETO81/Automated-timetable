import tkinter 
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import timetable_fac  # Import the timetable_fac module
import faculty
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")  # Themes: blue, dark-blue, or green

app = customtkinter.CTk()
app.geometry("600x640")
app.title("LOGIN")

# Set Background Image
image = Image.open(r'C:\Users\MOHD SUHAIL\Downloads\bg.jpg')
my_image = ImageTk.PhotoImage(image)
lbl = Label(image=my_image)
lbl.place(relheight=1, relwidth=1)

# Main Frame
frame = customtkinter.CTkFrame(master=app, width=320, height=460, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Title Label
l2 = customtkinter.CTkLabel(
    master=frame, text="WHAT WILL YOU TEACH", font=("Century Gothic", 20)
)
l2.place(x=18, y=45)

# Username Entry
entry1 = customtkinter.CTkEntry(master=frame,height=220, width=220, placeholder_text="COURSE INFO")
entry1.place(x=50, y=130)

# Function to open timetable
def open_timetable():
    # Call timetable_fac.fac_tt_frame here when the button is pressed
    # You may need to pass the course or faculty information as arguments, for now, I'm passing a placeholder
    timetable_fac.fac_tt_frame(app,faculty)  # Replace with the actual parameters if needed

# Login Button
button1 = customtkinter.CTkButton(
    master=frame, width=220, text="SUMBIT", corner_radius=6
)
button1.place(x=50, y=380)

# Open Timetable Button
button2 = customtkinter.CTkButton(
    master=frame, width=220, text="OPEN TIMETABLE", corner_radius=6, command=open_timetable
)
button2.place(x=50, y=420)

app.mainloop()
