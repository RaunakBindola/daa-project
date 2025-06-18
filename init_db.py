import sqlite3

# Connect to your Flask app's DB (it should be in the same directory)
conn = sqlite3.connect("timetable.db")
cursor = conn.cursor()

# Create the subjects table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher TEXT NOT NULL
    );
""")

conn.commit()
conn.close()

print("✅ Table 'subjects' created successfully.")
