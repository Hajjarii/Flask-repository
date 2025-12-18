import mariadb

DB_CONFIG = {
    "host": "localhost",
    "user": "Jonas",
    "password": "123123",
    "database": "infoskjerm"
}

def get_db_connection():
    return mariadb.connect(**DB_CONFIG)

def add_event(title, event_date, event_time, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO calendar_events (title, event_date, event_time, description) VALUES (?, ?, ?, ?)",
        (title, event_date, event_time, description)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT title, event_date, event_time, description FROM calendar_events ORDER BY event_date, event_time")
    events = cur.fetchall()
    cur.close()
    conn.close()
    return events