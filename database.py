import sqlite3

def create_connection():
    """Connect to (or create) the database file."""
    conn = sqlite3.connect("tracker.db")
    return conn

def create_table():
    """Create the applications table if it doesn't exist yet."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            salary TEXT,
            date_applied TEXT,
            status TEXT NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_application(company, role, location, salary, date_applied, status, notes):
    """Insert a new application into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (company, role, location, salary, date_applied, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (company, role, location, salary, date_applied, status, notes))
    conn.commit()
    conn.close()


def get_all_applications():
    """Return every application as a list of rows."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()
    conn.close()
    return rows 


def delete_application(app_id):
    """Delete one application by its id."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()

def update_status(app_id, new_status):
    """Change the status of one application."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()

def update_notes(app_id, new_notes):
    """Change the notes of one application."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET notes = ? WHERE id = ?", (new_notes, app_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    add_application("Google", "Software Engineer Intern", "London", "£50,000", "2026-10-01", "Applied", "Found via LinkedIn")
    add_application("IBM", "Data Analyst Placement", "Manchester", "£45,000", "2026-10-03", "Interview", "Phone screen next week")

    print("Current applications:")
    for row in get_all_applications():
        print(row)

