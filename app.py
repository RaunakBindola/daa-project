from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


def generate_dynamic_timetable(class_counts, days_per_week, slots_per_day, slot_timings):
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"][:days_per_week]
    timetable = []
    total_slots = days_per_week * slots_per_day

    # Create empty timetable grid
    grid = {day: [""] * slots_per_day for day in days}

    # Sort by least classes to distribute small ones first
    sorted_faculties = sorted(class_counts.items(), key=lambda x: x[1])

    from collections import deque

    available_slots = deque([(day, slot) for day in days for slot in range(slots_per_day)])

    for faculty, count in sorted_faculties:
        placed = 0
        used_days = set()

        while placed < count and available_slots:
            for _ in range(len(available_slots)):
                day, slot = available_slots[0]
                available_slots.rotate(-1)  # rotate to try next slot next time

                if grid[day][slot] == "" and day not in used_days:
                    grid[day][slot] = faculty
                    placed += 1
                    used_days.add(day)
                    break  # move to next class for this faculty

            # Reset used_days to allow reuse of days if needed
            if placed < count and len(used_days) == len(days):
                used_days = set()

    for day in days:
        timetable.append({"day": day, "slots": grid[day]})

    return timetable

def save_timetable_to_db(timetable, slot_timings):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS timetable_archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        slot_index INTEGER,
        timing TEXT,
        teacher TEXT
    )''')

    cursor.execute("DELETE FROM timetable_archive")  # Clear old for now (or skip this if you want to keep history)

    for row in timetable:
        for i, teacher in enumerate(row['slots']):
            cursor.execute(
                "INSERT INTO timetable_archive (day, slot_index, timing, teacher) VALUES (?, ?, ?, ?)",
                (row['day'], i, slot_timings[i], teacher)
            )
    conn.commit()
    conn.close()


# 👉 Route 1: Dashboard
@app.route('/')
def dashboard():
    return render_template("dashboard.html")

from flask import Flask, render_template, redirect, url_for, request


@app.route('/generate-timetable', methods=['GET', 'POST'])
def generate_timetable_route():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT teacher FROM subjects")
    faculties = [{"id": idx, "name": row[0]} for idx, row in enumerate(cursor.fetchall())]

    if request.method == 'POST':
        selected_ids = request.form.getlist('faculty_ids')
        faculty_name_map = {str(f["id"]): f["name"] for f in faculties}
        class_counts = {
            faculty_name_map[fid]: int(request.form.get(f'classes_{fid}'))
            for fid in selected_ids
        }

        slots_per_day = int(request.form['slots_per_day'])
        days_per_week = int(request.form['days_per_week'])  # 5 or 6
        slot_timings = [s.strip() for s in request.form['slot_timings'].split(',')]

        timetable = generate_dynamic_timetable(
            class_counts, days_per_week, slots_per_day, slot_timings
        )

        save_timetable_to_db(timetable, slot_timings)

        return render_template('timetable.html', timetable=timetable, slot_timings=slot_timings)

    return render_template('generate_timetable.html', faculties=faculties)

    # 👉 Route 3: View timetable
@app.route('/view-timetable')
def view_timetable():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT day, slot_index, timing, teacher
        FROM timetable_archive
        ORDER BY 
            CASE day 
                WHEN 'MON' THEN 1
                WHEN 'TUE' THEN 2
                WHEN 'WED' THEN 3
                WHEN 'THU' THEN 4
                WHEN 'FRI' THEN 5
                WHEN 'SAT' THEN 6
            END,
            slot_index
    """)
    rows = cursor.fetchall()
    conn.close()

    # Build list of unique timings in correct order
    slot_timings = []
    max_slots = 0
    for _, slot, timing, _ in rows:
        if len(slot_timings) <= slot:
            slot_timings.extend([""] * (slot - len(slot_timings) + 1))
        slot_timings[slot] = timing
        max_slots = max(max_slots, slot + 1)

    # Prepare empty timetable
    timetable = {}

    for day, slot, _, teacher in rows:
        if day not in timetable:
            timetable[day] = [""] * max_slots
        timetable[day][slot] = teacher

    final_timetable = [{"day": day, "slots": timetable[day]} for day in ["MON", "TUE", "WED", "THU", "FRI", "SAT"] if day in timetable]

    return render_template("timetable.html", timetable=final_timetable, slot_timings=slot_timings)





@app.route('/add-faculty', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        subject_name = request.form['subject']
        teacher_name = request.form['teacher']

        conn = sqlite3.connect('timetable.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", (subject_name, teacher_name))
        conn.commit()
        conn.close()

        return redirect(url_for('view'))  # After adding, go to timetable view

    return render_template('add_faculty.html')

@app.route('/faculty-list')
def faculty_list():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    conn.close()
    return render_template('faculty_list.html', subjects=subjects)


@app.route('/delete_faculty', methods=['GET', 'POST'])
def delete_faculty():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        selected_ids = request.form.getlist('faculty_ids')
        for fid in selected_ids:
            cursor.execute("DELETE FROM subjects WHERE rowid = ?", (fid,))
        conn.commit()
        conn.close()
        return redirect(url_for('delete_faculty'))

    cursor.execute("SELECT rowid, teacher FROM subjects")
    faculties = cursor.fetchall()
    conn.close()
    return render_template('delete_faculty.html', faculties=faculties)


if __name__ == "__main__":
    app.run(debug=True)
