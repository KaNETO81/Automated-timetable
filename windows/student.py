import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

fid = passw = conf_passw = name = roll = section = None


# Create treeview (call this function once)
def create_treeview():
    tree["columns"] = list(map(lambda x: '#' + str(x), range(1, 5)))
    tree.column("#0", width=0, stretch=ctk.NO)
    tree.column("#1", width=70, stretch=ctk.NO)
    tree.column("#2", width=200, stretch=ctk.NO)
    tree.column("#3", width=80, stretch=ctk.NO)
    tree.column("#4", width=80, stretch=ctk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="SID")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Roll")
    tree.heading('#4', text="Section")
    tree['height'] = 12


# Update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT SID, NAME, ROLL, SECTION FROM STUDENT")
    for row in cursor:
        tree.insert("", 0, values=(row[0], row[1], row[2], row[3]))
    tree.place(x=530, y=100)


# Parse and store data into database and treeview upon clicking the add button
def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    roll = str(roll_entry.get())
    section = str(sec_entry.get()).upper()

    if fid == "" or passw == "" or conf_passw == "" or name == "" or roll == "" or section == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didn't match. Try again!")
        passw_entry.delete(0, ctk.END)
        conf_passw_entry.delete(0, ctk.END)
        return

    conn.execute(f"REPLACE INTO STUDENT (SID, PASSW, NAME, ROLL, SECTION)\
        VALUES ('{fid}','{passw}','{name}', '{roll}', '{section}')")
    conn.commit()
    update_treeview()

    fid_entry.delete(0, ctk.END)
    passw_entry.delete(0, ctk.END)
    conf_passw_entry.delete(0, ctk.END)
    name_entry.delete(0, ctk.END)
    roll_entry.delete(0, ctk.END)
    sec_entry.delete(0, ctk.END)


# Update a row in the database
def update_data():
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one student at a time to update!")
            return

        if len(tree.selection()) < 1:
            messagebox.showerror("Bad Select", "Please select a student from the list first!")
            return

        # Fetch selected row's data
        selected_item = tree.selection()[0]
        q_fid = tree.item(selected_item)['values'][0]
        cursor = conn.execute(f"SELECT * FROM STUDENT WHERE SID = '{q_fid}'")
        result = list(cursor)

        if not result:
            messagebox.showerror("Error", "Student record not found!")
            return

        # Populate entry fields for editing
        fid_entry.delete(0, ctk.END)
        passw_entry.delete(0, ctk.END)
        conf_passw_entry.delete(0, ctk.END)
        name_entry.delete(0, ctk.END)
        roll_entry.delete(0, ctk.END)
        sec_entry.delete(0, ctk.END)

        fid_entry.insert(0, result[0][0])
        passw_entry.insert(0, result[0][1])
        conf_passw_entry.insert(0, result[0][1])
        name_entry.insert(0, result[0][2])
        roll_entry.insert(0, result[0][3])
        sec_entry.insert(0, result[0][4])

        # Confirm and save updates
        def save_update():
            new_fid = fid_entry.get()
            new_passw = passw_entry.get()
            new_conf_passw = conf_passw_entry.get()
            new_name = name_entry.get().upper()
            new_roll = roll_entry.get()
            new_section = sec_entry.get().upper()

            if new_passw != new_conf_passw:
                messagebox.showerror("Passwords mismatch", "Password and confirm password didn't match. Try again!")
                return

            conn.execute(f"""
                UPDATE STUDENT
                SET SID = ?, PASSW = ?, NAME = ?, ROLL = ?, SECTION = ?
                WHERE SID = ?
            """, (new_fid, new_passw, new_name, new_roll, new_section, q_fid))
            conn.commit()
            update_treeview()
            messagebox.showinfo("Success", "Student record updated successfully!")

        B1.configure(text="Save Update", command=save_update)

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return


# Remove selected data from database and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected record(s)?")
    if not confirm:
        return

    for item in tree.selection():
        fid = tree.item(item)['values'][0]
        conn.execute(f"DELETE FROM STUDENT WHERE SID = ?", (fid,))
        conn.commit()
        tree.delete(item)

    update_treeview()
    messagebox.showinfo("Success", "Selected student(s) deleted successfully!")


# Toggles between show/hide password
def show_passw():
    if passw_entry.cget('show') == "●":
        passw_entry.configure(show="")
        B1_show.configure(text='●')
    else:
        passw_entry.configure(show="●")
        B1_show.configure(text='○')


# Main
if __name__ == "__main__":

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # Connecting database
    conn = sqlite3.connect(r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db')

    # Creating Table in the database
    conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
    (SID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    ROLL INTEGER NOT NULL,\
    SECTION CHAR(5) NOT NULL)')

    '''
        customtkinter WINDOW SETUP WITH WIDGETS
    '''

    subtk = ctk.CTk()
    subtk.geometry('1000x470')
    subtk.title('Add/Update Students')

    ctk.CTkLabel(subtk, text='List of Students', font=('Consolas', 20, 'bold')).place(x=620, y=50)
    ctk.CTkLabel(subtk, text='Add/Update Students', font=('Consolas', 20, 'bold')).place(x=110, y=50)

    ctk.CTkLabel(subtk, text='Student id:', font=('Consolas', 12)).place(x=100, y=130)
    fid_entry = ctk.CTkEntry(subtk, font=('Consolas', 12), width=130)
    fid_entry.place(x=260, y=130)

    ctk.CTkLabel(subtk, text='Password:', font=('Consolas', 12)).place(x=100, y=170)
    passw_entry = ctk.CTkEntry(subtk, font=('Consolas', 12), width=130, show="●")
    passw_entry.place(x=260, y=170)

    B1_show = ctk.CTkButton(subtk, text='○', font=('Consolas', 9, 'bold'), width=40, command=show_passw)
    B1_show.place(x=400, y=170)

    ctk.CTkLabel(subtk, text='Confirm Password:', font=('Consolas', 12)).place(x=100, y=210)
    conf_passw_entry = ctk.CTkEntry(subtk, font=('Consolas', 12), width=130, show="●")
    conf_passw_entry.place(x=260, y=210)

    ctk.CTkLabel(subtk, text='Student Name:', font=('Consolas', 12)).place(x=100, y=250)
    name_entry = ctk.CTkEntry(subtk, font=('Consolas', 12), width=130)
    name_entry.place(x=260, y=250)

    ctk.CTkLabel(subtk, text='Roll no.:', font=('Consolas', 12)).place(x=100, y=290)
    roll_entry = ctk.CTkEntry(subtk, font=('Consolas', 12), width=130)
    roll_entry.place(x=260, y=290)

    ctk.CTkLabel(subtk, text='Branch:', font=('Consolas', 12)).place(x=100, y=330)
    sec_entry = ctk.CTkEntry(subtk, font=('Consolas', 12), width=130)
    sec_entry.place(x=260, y=330)

    B1 = ctk.CTkButton(subtk, text='Add Student', font=('Consolas', 12), command=parse_data)
    B1.place(x=150, y=400)

    B2 = ctk.CTkButton(subtk, text='Update Student', font=('Consolas', 12), command=update_data)
    B2.place(x=410, y=400)

    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    B3 = ctk.CTkButton(subtk, text='Delete Student(s)', font=('Consolas', 12), command=remove_data)
    B3.place(x=650, y=400)

    subtk.mainloop()
    conn.close()
