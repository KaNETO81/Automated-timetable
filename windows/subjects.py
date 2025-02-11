import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox

# Database connection
conn = sqlite3.connect(r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db')

# Create table in the database if it doesn't exist
conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS (SUBCODE CHAR(10) NOT NULL PRIMARY KEY, SUBNAME CHAR(50) NOT NULL, SUBTYPE CHAR(1) NOT NULL)')

# Function to create the Treeview
def create_treeview():
    tree['columns'] = ('one', 'two', 'three')
    tree.column("#0", width=0, stretch=ctk.NO)
    tree.column("one", width=70, stretch=ctk.NO)
    tree.column("two", width=300, stretch=ctk.NO)
    tree.column("three", width=60, stretch=ctk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Code")
    tree.heading('two', text="Name")
    tree.heading('three', text="Type")

# Function to update the Treeview
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM SUBJECTS")
    for row in cursor:
        t = 'Theory' if row[2] == 'T' else 'Practical'
        tree.insert("", 0, values=(row[0], row[1], t))

# Function to parse data from the GUI and add/update the database
def parse_data():
    subcode = str(subcode_entry.get())
    subname = str(subname_entry.get("1.0", ctk.END)).strip().upper()
    subtype = str(radio_var.get()).upper()

    if not subcode or not subname:
        messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
        return

    conn.execute("REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE) VALUES (?, ?, ?)", (subcode, subname, subtype))
    conn.commit()
    update_treeview()

    subcode_entry.delete(0, ctk.END)
    subname_entry.delete("1.0", ctk.END)

# Function to update selected subject in the database
def update_data():
    subcode_entry.delete(0, ctk.END)
    subname_entry.delete("1.0", ctk.END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        subcode_entry.insert(0, row[0])
        subname_entry.insert("1.0", row[1])
        radio_var.set(row[2][0])  # Set the radio button value

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")

# Function to remove selected subjects from the database
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return
    for i in tree.selection():
        conn.execute("DELETE FROM SUBJECTS WHERE SUBCODE = ?", (tree.item(i)['values'][0],))
        conn.commit()
    update_treeview()

# Main application
if __name__ == "__main__":
    # Set up customtkinter window
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    subtk = ctk.CTk()
    subtk.geometry('1000x450')
    subtk.title('Add/Update Subjects')

    # Labels and Entries
    ctk.CTkLabel(subtk, text='List of Subjects', font=('Consolas', 20, 'bold')).place(x=600, y=50)
    ctk.CTkLabel(subtk, text='Add/Update Subjects', font=('Consolas', 20, 'bold')).place(x=100, y=50)
    ctk.CTkLabel(subtk, text='Add information in the following prompt!', font=('Consolas', 10, 'italic')).place(x=100, y=85)

    ctk.CTkLabel(subtk, text='Subject code:', font=('Consolas', 15)).place(x=100, y=150)
    subcode_entry = ctk.CTkEntry(subtk, font=('Consolas', 15), width=200)
    subcode_entry.place(x=270, y=150)

    ctk.CTkLabel(subtk, text='Subject Name:', font=('Consolas', 15)).place(x=100, y=200)
    subname_entry = ctk.CTkTextbox(subtk, font=('Consolas', 12), width=200, height=50)
    subname_entry.place(x=270, y=200)

    ctk.CTkLabel(subtk, text='Subject Type:', font=('Consolas', 15)).place(x=100, y=270)
    radio_var = ctk.StringVar(value="T")  # Default selection

    R1 = ctk.CTkRadioButton(subtk, text='Theory', font=('Consolas', 12), variable=radio_var, value="T")
    R1.place(x=270, y=270)

    R2 = ctk.CTkRadioButton(subtk, text='Practical', font=('Consolas', 12), variable=radio_var, value="P")
    R2.place(x=270, y=300)

    ctk.CTkButton(subtk, text='Add Subject', font=('Consolas', 12), command=parse_data).place(x=150, y=350)
    ctk.CTkButton(subtk, text='Update Subject', font=('Consolas', 12), command=update_data).place(x=410, y=350)

    # Treeview for subjects (using ttk)
    tree_frame = ctk.CTkFrame(subtk, width=450, height=250)
    tree_frame.place(x=500, y=100)
    tree = ttk.Treeview(tree_frame)
    tree.pack(fill="both", expand=True)
    create_treeview()
    update_treeview()

    ctk.CTkButton(subtk, text='Delete Subject(s)', font=('Consolas', 12), command=remove_data).place(x=650, y=350)

    # Start customtkinter main loop
    subtk.mainloop()
    conn.close()  # Close the database after all operations
