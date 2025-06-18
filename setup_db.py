import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('timetable.db')
cursor = conn.cursor()

# Create Subjects Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher TEXT NOT NULL
)
""")

# Create Timetable Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    day TEXT,
    slot INTEGER,
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")

conn.commit()
conn.close()
print("Database and tables created successfully.")
