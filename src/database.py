import sqlite3

DATABASE_PATH = "consultbae.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            city TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS naukri_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            source_row INTEGER,
            experience_years REAL,
            current_ctc TEXT,
            applied_date TEXT,
            skills TEXT,
            FOREIGN KEY (person_id) REFERENCES people(person_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gig_worker_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            source_row INTEGER,
            rate TEXT,
            status TEXT,
            skill_tags TEXT,
            FOREIGN KEY (person_id) REFERENCES people(person_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cbnexus_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            source_row INTEGER,
            verified TEXT,
            projects_completed INTEGER,
            FOREIGN KEY (person_id) REFERENCES people(person_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            source TEXT,
            source_row INTEGER,
            match_score INTEGER,
            match_type TEXT,
            notes TEXT,
            FOREIGN KEY (person_id) REFERENCES people(person_id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database schema created successfully.")