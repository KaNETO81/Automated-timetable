import customtkinter as ctk
import sqlite3

# Constants for timetable structure
days = 6
periods = 7
recess_break_after = 4
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
period_names = list(map(lambda x: 'Period ' + str(x), range(1, 8)))

# Database connection
conn = sqlite3.connect(r"C:\Users\MOHD SUHAIL\mini pj\TimeTable-Generator-\files\timetable.db")
butt_grid = []
section = None


def select_section():
    """Fetch and display timetable for the selected section."""
    global section
    section = section_combo.get()
    update_table(section)


def update_table(sec):
    """Update timetable buttons based on the database data for the given section."""
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(
                f"SELECT SUBCODE, FINI FROM SCHEDULE WHERE DAYID={i} AND PERIODID={j} AND SECTION='{sec}'"
            )
            result = list(cursor)

            butt_grid[i][j].configure(text="No Class", fg_color="gray", text_color="black")

            if result:
                subcode, fini = result[0]
                subject_cursor = conn.execute(f"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                subtype = list(subject_cursor)[0][0]

                # Assign colors based on type
                color = "green" if subtype == 'T' else "blue"
                butt_grid[i][j].configure(
                    text=f"{subcode}\n{fini}",
                    fg_color=color,
                    text_color="white"
                )


def process_button(d, p):
    """Display class details when a timetable button is clicked."""
    details = ctk.CTkToplevel()
    details.title("Class Details")
    details.geometry("400x300")

    cursor = conn.execute(
        f"SELECT SUBCODE, FINI FROM SCHEDULE WHERE DAYID={d} AND PERIODID={p} AND SECTION='{section}'"
    )
    result = list(cursor)

    if result:
        subcode, fini = result[0]
        subject_cursor = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
        subname, subtype = list(subject_cursor)[0]

        faculty_cursor = conn.execute(f"SELECT NAME, EMAIL FROM FACULTY WHERE INI='{fini}'")
        faculty_result = list(faculty_cursor)

        if faculty_result:
            fname, femail = faculty_result[0]
        else:
            fname, femail = "Faculty not found", "Unknown"

        subtype_full = "Theory" if subtype == "T" else "Practical"
    else:
        subcode = subname = subtype_full = fname = femail = "None"
        fini = "N/A"

    details_content = [
        f"Day: {day_names[d]}",
        f"Period: {period_names[p]}",
        f"Subject Code: {subcode}",
        f"Subject Name: {subname}",
        f"Subject Type: {subtype_full}",
        f"Faculty Initials: {fini}",
        f"Faculty Name: {fname}",
        f"Faculty Email: {femail}",
    ]

    for text in details_content:
        ctk.CTkLabel(details, text=text, font=("Consolas", 12)).pack(pady=5)

    ctk.CTkButton(details, text="OK", command=details.destroy).pack(pady=10)


def create_timetable_frame(root):
    """Create and display the timetable interface in two frames."""
    global butt_grid

    # Title
    title_label = ctk.CTkLabel(
        root, text="T I M E T A B L E", font=("Consolas", 20, "bold")
    )
    title_label.pack(pady=10)

    # Legend
    legend_frame = ctk.CTkFrame(root)
    legend_frame.pack(pady=10)

    ctk.CTkLabel(legend_frame, text="Legend:").pack(side="left", padx=5)
    ctk.CTkLabel(legend_frame, text="Theory Classes", fg_color="green", text_color="white", width=120).pack(side="left", padx=10)
    ctk.CTkLabel(legend_frame, text="Practical Classes", fg_color="blue", text_color="white", width=120).pack(side="left", padx=10)

    # Main timetable container
    timetable_container = ctk.CTkFrame(root)
    timetable_container.pack(pady=10)

    # Frames for first half and second half
    first_half_frame = ctk.CTkFrame(timetable_container)
    first_half_frame.pack(side="left", padx=10, pady=10)

    second_half_frame = ctk.CTkFrame(timetable_container)
    second_half_frame.pack(side="left", padx=10, pady=10)

    # First half: Periods 1 to 4
    for i, day in enumerate(day_names):
        ctk.CTkLabel(
            first_half_frame, text=day, font=("Consolas", 12, "bold")
        ).grid(row=i + 1, column=0, padx=5, pady=5)

    for j in range(4):  # Periods 1 to 4
        ctk.CTkLabel(
            first_half_frame, text=period_names[j], font=("Consolas", 12, "bold")
        ).grid(row=0, column=j + 1, padx=5, pady=5)

    for i in range(days):
        row_buttons = []
        for j in range(4):  # Periods 1 to 4
            btn = ctk.CTkButton(
                first_half_frame,
                text="No Class",
                width=120,
                height=50,
                fg_color="gray",
                text_color="black",
                command=lambda x=i, y=j: process_button(x, y)
            )
            btn.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            row_buttons.append(btn)
        butt_grid.append(row_buttons)

    # Second half: Periods 5 to 7
    for i, day in enumerate(day_names):
        ctk.CTkLabel(
            second_half_frame, text=day, font=("Consolas", 12, "bold")
        ).grid(row=i + 1, column=0, padx=5, pady=5)

    for j in range(4, periods):  # Periods 5 to 7
        ctk.CTkLabel(
            second_half_frame, text=period_names[j], font=("Consolas", 12, "bold")
        ).grid(row=0, column=j - 3, padx=5, pady=5)  # Offset column by 3 for proper alignment

    for i in range(days):
        for j in range(4, periods):  # Periods 5 to 7
            btn = ctk.CTkButton(
                second_half_frame,
                text="No Class",
                width=120,
                height=50,
                fg_color="gray",
                text_color="black",
                command=lambda x=i, y=j: process_button(x, y)
            )
            btn.grid(row=i + 1, column=j - 3, padx=5, pady=5)  # Offset column by 3 for proper alignment
            butt_grid[i].append(btn)  # Append to the same row in `butt_grid`


# Main code
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    tt = ctk.CTk()
    tt.title("Timetable")
    tt.geometry("1200x600")

    create_timetable_frame(tt)

    section_frame = ctk.CTkFrame(tt)
    section_frame.pack(pady=15)

    # ctk.CTkLabel(section_frame, text="Select Section:", font=("Consolas", 12)).pack(side="left", padx=10)

    cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
    sections = [row[0] for row in cursor]
    section_combo = ctk.CTkComboBox(section_frame, values=sections)
    section_combo.pack(side="left", padx=10)
    section_combo.set(sections[0] if sections else "None")

    ctk.CTkButton(section_frame, text="Load", command=select_section).pack(side="left", padx=10)

    tt.mainloop()
