import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Variables for admin fields
aid = passw = conf_passw = name = email = None

# Function to create the Treeview for Admins
def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 4)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.column("#3", width=200, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="Admin ID")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Email")
    tree['height'] = 12

# Function to update the Treeview with Admin data
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT AID, NAME, EMAIL FROM ADMIN")
    for row in cursor:
        tree.insert("", 0, values=(row[0], row[1], row[2]))
    tree.place(x=530, y=100)

# Function to parse and add Admin data
def parse_data():
    aid = str(aid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    email = str(email_entry.get()).lower()

    if aid == "" or passw == "" or conf_passw == "" or name == "" or email == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords Mismatch", "Password and confirm password didn't match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    conn.execute(f"REPLACE INTO ADMIN (AID, PASSW, NAME, EMAIL) VALUES ('{aid}', '{passw}', '{name}', '{email}')")
    conn.commit()
    update_treeview()

    aid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Function to update Admin data
def update_data():
    aid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one admin at a time to update!")
            return

        q_aid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM ADMIN WHERE AID = '{q_aid}'")

        cursor = list(cursor)
        aid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        email_entry.insert(0, cursor[0][3])

        conn.execute(f"DELETE FROM ADMIN WHERE AID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select an admin from the list first!")
        return

# Function to remove Admin data
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select an admin from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM ADMIN WHERE AID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()

# Main function
if __name__ == "__main__":

    # Database connection
    conn = sqlite3.connect(r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db')

    # Create ADMIN table if it does not exist
    conn.execute('''CREATE TABLE IF NOT EXISTS ADMIN (
        AID CHAR(10) NOT NULL PRIMARY KEY,
        PASSW CHAR(50) NOT NULL,
        NAME CHAR(50) NOT NULL,
        EMAIL CHAR(50) NOT NULL)''')

    # Tkinter Window Setup
    admin_tk = tk.Tk()
    admin_tk.geometry('1000x470')
    admin_tk.title('Admin Management')

    # Labels and Entries for Admin Information
    tk.Label(admin_tk, text='Admin Management', font=('Consolas', 20, 'bold')).place(x=110, y=50)

    tk.Label(admin_tk, text='Admin ID:', font=('Consolas', 12)).place(x=100, y=130)
    aid_entry = tk.Entry(admin_tk, font=('Consolas', 12), width=20)
    aid_entry.place(x=260, y=130)

    tk.Label(admin_tk, text='Password:', font=('Consolas', 12)).place(x=100, y=170)
    passw_entry = tk.Entry(admin_tk, font=('Consolas', 12), width=20, show="●")
    passw_entry.place(x=260, y=170)

    tk.Label(admin_tk, text='Confirm Password:', font=('Consolas', 12)).place(x=100, y=210)
    conf_passw_entry = tk.Entry(admin_tk, font=('Consolas', 12), width=20, show="●")
    conf_passw_entry.place(x=260, y=210)

    tk.Label(admin_tk, text='Name:', font=('Consolas', 12)).place(x=100, y=250)
    name_entry = tk.Entry(admin_tk, font=('Consolas', 12), width=25)
    name_entry.place(x=260, y=250)

    tk.Label(admin_tk, text='Email:', font=('Consolas', 12)).place(x=100, y=290)
    email_entry = tk.Entry(admin_tk, font=('Consolas', 12), width=30)
    email_entry.place(x=260, y=290)

    # Buttons for Admin Management
    tk.Button(admin_tk, text='Add Admin', font=('Consolas', 12), command=parse_data).place(x=150, y=400)
    tk.Button(admin_tk, text='Update Admin', font=('Consolas', 12), command=update_data).place(x=410, y=400)
    tk.Button(admin_tk, text='Delete Admin(s)', font=('Consolas', 12), command=remove_data).place(x=650, y=400)

    # Treeview for Displaying Admin Data
    tree = ttk.Treeview(admin_tk)
    create_treeview()
    update_treeview()

    # Run Tkinter Window
    admin_tk.mainloop()

    # Close the database connection
    conn.close()
