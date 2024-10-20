import sqlite3

# Create or connect to a local database
def setup_local_database():
    conn = sqlite3.connect('sproctor_offline.db')  # Create SQLite DB file
    cursor = conn.cursor()

    # Create table for storing behavior logs
    cursor.execute('''CREATE TABLE IF NOT EXISTS behavior_logs
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       student_id TEXT,
                       timestamp TEXT,
                       behavior TEXT,
                       cheat_probability REAL)''')

    conn.commit()
    conn.close()

# Insert behavior log into the local database
def log_behavior(student_id, behavior, cheat_probability):
    conn = sqlite3.connect('sproctor_offline.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO behavior_logs (student_id, timestamp, behavior, cheat_probability) VALUES (?, datetime('now'), ?, ?)", 
                   (student_id, behavior, cheat_probability))

    conn.commit()
    conn.close()
