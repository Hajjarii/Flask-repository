from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    mysql.init_app(app)

def get_user_by_username(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE username=%s", (username,))
    result = cur.fetchone()
    cur.close()
    return result

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE id=%s", (user_id,))
    result = cur.fetchone()
    cur.close()
    return result

def create_user(username, password_hash):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    mysql.connection.commit()
    cur.close()

def get_events_for_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, event_date, event_time, description FROM calendar_events WHERE user_id = %s", (user_id,))
    events = cur.fetchall()
    cur.close()
    return events

def add_event(user_id, title, event_date, event_time, description):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO calendar_events (user_id, title, event_date, event_time, description) VALUES (%s, %s, %s, %s, %s)",
        (user_id, title, event_date, event_time, description)
    )
    mysql.connection.commit()
    cur.close()