import os
import sqlite3

def sync_data_to_server():
    if check_internet_connection():
        conn = sqlite3.connect('sproctor_offline.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM behavior_logs")
        logs = cursor.fetchall()

        for log in logs:
            # Simulate uploading logs to the server
            print(f"Syncing log: {log}")
            # Code to upload log to the server can be added here

        # Clear local logs after successful sync
        cursor.execute("DELETE FROM behavior_logs")
        conn.commit()
        conn.close()
    else:
        print("No internet connection. Data will be synced later.")

def check_internet_connection():
    # Use os.system to ping a public DNS server to check internet connection
    return os.system("ping -c 1 google.com") == 0
