from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SLOTS_PER_DAY = 4

def generate_timetable():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, teacher FROM subjects")
    subjects = cursor.fetchall()
    graph = {sub[0]: set() for sub in subjects}
    for i in range(len(subjects)):
        for j in range(i + 1, len(subjects)):
            id1, teacher1 = subjects[i]
            id2, teacher2 = subjects[j]
            if teacher1 == teacher2:
                graph[id1].add(id2)
                graph[id2].add(id1)
    color = {}
    max_slots = SLOTS_PER_DAY * len(DAYS)
    for node in graph:
        used = {color.get(neigh) for neigh in graph[node] if neigh in color}
        for c in range(max_slots):
            if c not in used:
                color[node] = c
                break
    cursor.execute("DELETE FROM timetable")
    for sub_id, c in color.items():
        day = DAYS[c // SLOTS_PER_DAY]
        slot = c % SLOTS_PER_DAY
        cursor.execute("INSERT INTO timetable (subject_id, day, slot) VALUES (?, ?, ?)", (sub_id, day, slot))
    conn.commit()
    conn.close()

# 👉 Route 1: Dashboard
@app.route('/')
def dashboard():
    return render_template("dashboard.html")

# 👉 Route 2: Generate timetable
@app.route('/generate')
def generate():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    # Clear previous timetable
    cursor.execute("DELETE FROM timetable")

    # Get all subjects
    cursor.execute("SELECT id FROM subjects")
    subjects = [row[0] for row in cursor.fetchall()]

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    slots = [1, 2, 3, 4, 5]  # e.g., 5 slots per day

    timetable = []
    i = 0

    for day in days:
        for slot in slots:
            if i < len(subjects):
                timetable.append((subjects[i], day, slot))
                i += 1
            else:
                break

    # Save the generated timetable
    for entry in timetable:
        cursor.execute("INSERT INTO timetable (subject_id, day, slot) VALUES (?, ?, ?)", entry)

    conn.commit()
    conn.close()

    return redirect(url_for('view'))  # Redirect to view timetable


# 👉 Route 3: View timetable
@app.route('/view')
def view():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subjects.name, subjects.teacher, timetable.day, timetable.slot
        FROM timetable
        JOIN subjects ON timetable.subject_id = subjects.id
        ORDER BY timetable.day, timetable.slot
    """)
    timetable = cursor.fetchall()
    conn.close()
    return render_template("view.html", timetable=timetable)

from flask import render_template, request, redirect, url_for
import sqlite3

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



if __name__ == "__main__":
    app.run(debug=True)
