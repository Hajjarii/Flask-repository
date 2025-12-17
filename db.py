import mariadb
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'velg-en-sterk-hemmelig-nøkkel'

DB_CONFIG = {
    "host": "localhost",
    "user": "Jonas",
    "password": "123123",
    "database": "infoskjerm"
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
            session['username'] = username
            return redirect(url_for('calendar'))
        else:
            flash('Feil brukernavn eller passord.')
    return '''
    <form method="post">
        <input name="username" placeholder="Brukernavn" required>
        <input name="password" type="password" placeholder="Passord" required>
        <button type="submit">Logg inn</button>
    </form>
    '''

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
    event_list = ''.join(f"<li>{e[0]}: {e[1]}</li>" for e in events)
    return f'''
    <h2>Velkommen, {session['username']}!</h2>
    <form method="post">
        <input name="event_date" type="date" required>
        <input name="event_text" placeholder="Hva skal du gjøre?" required>
        <button type="submit">Lagre hendelse</button>
    </form>
    <ul>{event_list}</ul>
    <a href="{url_for('logout')}">Logg ut</a>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)