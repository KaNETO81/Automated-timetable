import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3

days = 6
periods = 7
recess_break_aft = 4  # recess after 3rd Period
fini = None
butt_grid = []

period_names = list(map(lambda x: 'Period ' + str(x), range(1, 6 + 2)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Connect to SQLite database
conn = sqlite3.connect(r"C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db")


def select_fac():
    global fini
    fini = str(combo1.get())
    update_table(fini)


def update_table(fini):
    for i in range(days):
        for j in range(periods):
            # Ensure that butt_grid is properly populated before accessing it
            if i < len(butt_grid) and j < len(butt_grid[i]):
                cursor = conn.execute(
                    f"SELECT SECTION, SUBCODE FROM SCHEDULE WHERE DAYID={i} AND PERIODID={j} AND FINI='{fini}'"
                )
                cursor = list(cursor)

                butt_grid[i][j].configure(text="No Class")
                if len(cursor) != 0:
                    subcode = cursor[0][1]
                    cur1 = conn.execute(f"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                    cur1 = list(cur1)
                    subtype = cur1[0][0]

                    if subtype == 'T':
                        butt_grid[i][j].configure(fg_color="red", text_color="white")
                    elif subtype == 'P':
                        butt_grid[i][j].configure(fg_color="yellow", text_color="black")

                    sec_li = [x[0] for x in cursor]
                    t = ', '.join(sec_li)
                    butt_grid[i][j].configure(text=f"Sections: {t}")


def process_button(d, p):
    details = ctk.CTkToplevel()
    details.title("Class Details")
    details.geometry("400x400")

    cursor = conn.execute(
        f"SELECT SECTION, SUBCODE FROM SCHEDULE WHERE DAYID={d} AND PERIODID={p} AND FINI='{fini}'"
    )
    cursor = list(cursor)

    sec_li, subcode, subname, subtype = "None", "None", "None", "None"
    if cursor:
        sec_li = [x[0] for x in cursor]
        subcode = cursor[0][1]
        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = cur1[0][0]
        subtype = "Theory" if cur1[0][1] == 'T' else "Practical"

    labels = [
        f"Day: {day_names[d]}",
        f"Period: {p + 1}",
        f"Subject Code: {subcode}",
        f"Subject Name: {subname}",
        f"Subject Type: {subtype}",
        f"Faculty Initials: {fini}",
        f"Sections: {', '.join(sec_li) if isinstance(sec_li, list) else sec_li}",
        "Class Time: 50 minutes",
    ]

    for label in labels:
        ctk.CTkLabel(details, text=label, anchor="w", font=("Consolas", 12)).pack(fill="x", padx=20, pady=5)

    ctk.CTkButton(details, text="OK", command=details.destroy).pack(pady=20)


def fac_tt_frame(tt, f):
    global butt_grid  # Use the global variable to ensure it's accessed correctly
    butt_grid = []  # Clear butt_grid to avoid reusing any old data

    title_lab = ctk.CTkLabel(tt, text="T I M E T A B L E", font=("Consolas", 20, "bold"))
    title_lab.pack(pady=10)

    info_frame = ctk.CTkFrame(tt)
    info_frame.pack(pady=10)

    ctk.CTkLabel(info_frame, text="Theory Classes", fg_color="red", text_color="white", width=120).pack(side="left", padx=10)
    ctk.CTkLabel(info_frame, text="Practical Classes", fg_color="yellow", text_color="black", width=120).pack(side="left", padx=10)

    global fini
    fini = f

    table_frame = ctk.CTkFrame(tt)
    table_frame.pack(pady=10)

    first_half = ctk.CTkFrame(table_frame)
    first_half.pack(side="left", padx=20)

    recess_frame = ctk.CTkFrame(table_frame)
    recess_frame.pack(side="left", padx=20)

    second_half = ctk.CTkFrame(table_frame)
    second_half.pack(side="left", padx=20)

    # Recess section (Lunch break) placed between the two frames
    lunch_label = ctk.CTkLabel(
        recess_frame,
        text="L\n\nU\n\nN\n\nC\n\nH\n\n1hr.",
        font=("Consolas", 18, "italic"),
        width=3,
        height=10,
        corner_radius=10,
        fg_color="lightgray",
        text_color="black",
        anchor="center",
    )
    lunch_label.pack(padx=5, pady=5)

    # First half (Period 1 to 4)
    for i in range(days):
        day_label = ctk.CTkLabel(first_half, text=day_names[i], font=("Consolas", 12, "bold"), width=15)
        day_label.grid(row=i + 1, column=0, padx=5, pady=5)

    for j in range(4):  # Periods 1 to 4
        period_label = ctk.CTkLabel(first_half, text=period_names[j], font=("Consolas", 12, "bold"), width=15)
        period_label.grid(row=0, column=j + 1, padx=5, pady=5)

    # Add buttons for Periods 1 to 4 in first half
    for i in range(days):
        row_buttons = []
        for j in range(4):  # Periods 1 to 4
            btn = ctk.CTkButton(
                first_half,
                text="No Class",
                width=120,
                height=50,
                 text_color="white",  # Set the text color to white
                command=lambda x=i, y=j: process_button(x, y),
            )
            btn.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            row_buttons.append(btn)
        butt_grid.append(row_buttons)

    # Second half (Period 5 to 7)
    for i in range(days):
        row_buttons = []
        for j in range(4, periods):  # Periods 5 to 7
            btn = ctk.CTkButton(
                second_half,
                text="No Class",
                width=120,
                height=50,
                text_color="white",
                command=lambda x=i, y=j: process_button(x, y),
            )
            btn.grid(row=i + 1, column=j - 3, padx=5, pady=5)
            row_buttons.append(btn)
        butt_grid.append(row_buttons)

    for j in range(4):  # Periods 1 to 4
        period_label = ctk.CTkLabel(first_half, text=period_names[j], font=("Consolas", 12, "bold"), width=15)
        period_label.grid(row=0, column=j + 1, padx=5, pady=5)

    for j in range(4, periods):  # Periods 5 to 7
        period_label = ctk.CTkLabel(second_half, text=period_names[j], font=("Consolas", 12, "bold"), width=15)
        period_label.grid(row=0, column=j - 3, padx=5, pady=5)

    # Now call update_table after the grid is populated
    update_table(fini)


# Main code to run the app
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    tt = ctk.CTk()
    tt.title("Faculty Timetable")
    tt.geometry("1200x520")

    fac_tt_frame(tt, fini)

    fac_select_frame = ctk.CTkFrame(tt)
    fac_select_frame.pack(pady=10)

    ctk.CTkLabel(fac_select_frame, text="Select Faculty:", font=("Consolas", 12, "bold")).pack(side="left", padx=5)

    cursor = conn.execute("SELECT DISTINCT INI FROM FACULTY")
    fac_list = [row[0] for row in cursor]
    combo1 = ttk.Combobox(fac_select_frame, values=fac_list)
    combo1.pack(side="left", padx=5)
    combo1.current(0)

    ctk.CTkButton(fac_select_frame, text="OK", command=select_fac).pack(side="left", padx=5)

    select_fac()
    tt.mainloop()