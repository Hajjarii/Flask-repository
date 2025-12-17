import mariadb
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'velg-en-sterk-hemmelig-nøkkel'

DB_CONFIG = {
    "host": "localhost",
    "user": "din_db_bruker",
    "password": "ditt_db_passord",
    "database": "din_db"
}

def get_db_connection():
    return mariadb.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and password == user[1]:
            session['user_id'] = user[0]
            return redirect(url_for('calendar'))
        else:
            flash('Feil brukernavn eller passord.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            flash('Bruker registrert! Logg inn.')
            return redirect(url_for('login'))
        except mariadb.IntegrityError:
            flash('Brukernavn er allerede i bruk.')
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        event_date = request.form['event_date']
        event_text = request.form['event_text']
        cur.execute("INSERT INTO calendar_events (user_id, event_date, event_text) VALUES (?, ?, ?)", (user_id, event_date, event_text))
        conn.commit()
    cur.execute("SELECT event_date, event_text FROM calendar_events WHERE user_id=? ORDER BY event_date", (user_id,))
    events = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('calendar.html', events=events)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)