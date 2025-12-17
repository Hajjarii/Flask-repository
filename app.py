from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import db

app = Flask(__name__)
app.secret_key = 'velg-en-sterk-hemmelig-nøkkel'

login_form = '''
<form method="post">
    <input name="username" placeholder="Brukernavn" required>
    <input name="password" type="password" placeholder="Passord" required>
    <button type="submit">Logg inn</button>
</form>
'''

calendar_form = '''
<h2>Velkommen, {{username}}!</h2>
<form method="post">
    <input name="event_date" type="date" required>
    <input name="event_text" placeholder="Hva skal du gjøre?" required>
    <button type="submit">Lagre hendelse</button>
</form>
<ul>
    {% for e in events %}
        <li>{{e[0]}}: {{e[1]}}</li>
    {% endfor %}
</ul>
<a href="{{ url_for('logout') }}">Logg ut</a>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(username)
        if user and password == user[1]:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('calendar'))
        else:
            flash('Feil brukernavn eller passord.')
    return render_template_string(login_form)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    if request.method == 'POST':
        event_date = request.form['event_date']
        event_text = request.form['event_text']
        db.add_event(user_id, event_date, event_text)
    events = db.get_events(user_id)
    return render_template_string(calendar_form, events=events, username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)