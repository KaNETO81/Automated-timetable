import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random

# Constants
days = 6  # Monday to Saturday
periods = 7  # 7 periods per day
recess_break_aft = 4  # Lunch break after the 4th period
section = None  # Holds the selected section
butt_grid = []

period_names = [f'Period {x}' for x in range(1, 8)]  # Periods 1 to 7
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Database connection
conn = sqlite3.connect(r'C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db')

# Ensure the SCHEDULE table exists
conn.execute('''CREATE TABLE IF NOT EXISTS SCHEDULE (
    ID CHAR(10) NOT NULL PRIMARY KEY,
    DAYID INT NOT NULL,
    PERIODID INT NOT NULL,
    SUBCODE CHAR(10) NOT NULL,
    SECTION CHAR(5) NOT NULL,
    FINI CHAR(10) NOT NULL
)''')

def auto_generate_timetable():
    global section
    if not section or section.strip() == "":
        messagebox.showerror("Error", "No section selected! Please select a section first.")
        return

    # Clear existing schedule for the section
    conn.execute("DELETE FROM SCHEDULE WHERE SECTION=?", (section,))
    conn.commit()

    # Fetch available subjects and faculty
    cursor = conn.execute("""
        SELECT SUBJECTS.SUBCODE, FACULTY.INI
        FROM SUBJECTS
        JOIN FACULTY
        ON REPLACE(FACULTY.SUBCODE1, '-', '') = SUBJECTS.SUBCODE
        OR REPLACE(FACULTY.SUBCODE2, '-', '') = SUBJECTS.SUBCODE
    """)
    subject_faculty_pairs = cursor.fetchall()

    if not subject_faculty_pairs:
        messagebox.showerror("Error", "No subjects or faculty available for scheduling!")
        return

    # Distribute subjects across the timetable
    for day in range(days):
        assigned_periods = set()
        for _ in range(periods):
            while True:
                period = random.randint(0, periods - 1)
                if period not in assigned_periods:  # Avoid duplicate periods
                    assigned_periods.add(period)
                    break

            # Assign a random subject and faculty
            sub_fac = random.choice(subject_faculty_pairs)
            subcode, faculty_ini = sub_fac

            conn.execute("""
                INSERT INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (f"{section}{day}{period}", day, period, subcode, section, faculty_ini))

    conn.commit()
    update_table()
    messagebox.showinfo("Success", f"Timetable generated successfully for section {section}!")

def update_table():
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute("SELECT SUBCODE, FINI FROM SCHEDULE WHERE DAYID=? AND PERIODID=? AND SECTION=?", (i, j, section))
            result = cursor.fetchone()
            if result:
                butt_grid[i][j]['text'] = f'{result[0]}\n{result[1]}'
            else:
                butt_grid[i][j]['text'] = "No Class"
            butt_grid[i][j].update()

def select_sec():
    global section
    section = combo1.get()
    if not section:
        messagebox.showerror("Error", "Please select a valid section!")
        return
    update_table()

# Main application
tt = tk.Tk()
tt.title('Scheduler')

tk.Label(tt, text='T  I  M  E  T  A  B  L  E', font=('Consolas', 20, 'bold'), pady=5).pack()

table = tk.Frame(tt)
table.pack()

first_half = tk.Frame(table)
first_half.pack(side='left')

recess_frame = tk.Frame(table)
recess_frame.pack(side='left')

second_half = tk.Frame(table)
second_half.pack(side='left')

recess = tk.Label(recess_frame, text='L\n\nU\n\nN\n\nC\n\nH', font=('Consolas', 18, 'italic'), width=3, relief='sunken')
recess.pack()

for i in range(days):
    tk.Label(first_half, text=day_names[i], font=('Consolas', 12, 'bold'), width=9, height=2, bd=5, relief='raised').grid(row=i+1, column=0)

for i in range(periods):
    frame = first_half if i < recess_break_aft else second_half
    tk.Label(frame, text=period_names[i], font=('Consolas', 12, 'bold'), width=9, height=1, bd=5, relief='raised').grid(row=0, column=i+1)

for i in range(days):
    b = []
    for j in range(periods):
        frame = first_half if j < recess_break_aft else second_half
        bb = tk.Button(frame, text='No Class', font=('Consolas', 10), width=13, height=3, bd=5, relief='raised', wraplength=80, justify='center')
        bb.grid(row=i+1, column=j+1)
        b.append(bb)

    butt_grid.append(b)

sec_select_f = tk.Frame(tt, pady=15)
sec_select_f.pack()

tk.Label(sec_select_f, text='Select section: ', font=('Consolas', 12, 'bold')).pack(side=tk.LEFT)

cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
sec_li = [row[0] for row in cursor]
combo1 = ttk.Combobox(sec_select_f, values=sec_li)
combo1.pack(side=tk.LEFT)
combo1.current(0)

tk.Button(sec_select_f, text="OK", font=('Consolas', 12, 'bold'), padx=10, command=select_sec).pack(side=tk.LEFT, padx=10)

tk.Button(sec_select_f, text="Auto Generate", font=('Consolas', 12, 'bold'), padx=10, command=auto_generate_timetable).pack(side=tk.LEFT, padx=10)

update_table()

tt.mainloop()
