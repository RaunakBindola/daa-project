import sqlite3

# Connect to the existing timetable.db
conn = sqlite3.connect('timetable.db')
cursor = conn.cursor()

# Sample subjects and teachers
subjects = [
    ("Math", "Mr. A"),
    ("Science", "Ms. B"),
    ("English", "Mr. C"),
    ("History", "Ms. D"),
    ("Geography", "Mr. E"),
    ("Computer", "Ms. F")
]

# Insert the data
cursor.executemany("INSERT INTO subjects (name, teacher) VALUES (?, ?)", subjects)
conn.commit()
conn.close()

print("Sample data inserted successfully.")
