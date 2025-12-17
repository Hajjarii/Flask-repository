from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import db

app = Flask(__name__)
app.secret_key = 'velg-en-sterk-hemmelig-nøkkel'

# MariaDB config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'din_db_bruker'
app.config['MYSQL_PASSWORD'] = 'ditt_db_passord'
app.config['MYSQL_DB'] = 'din_db'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get_by_username(username):
        result = db.get_user_by_username(username)
        if result:
            return User(*result)
        return None

    @staticmethod
    def get_by_id(user_id):
        result = db.get_user_by_id(user_id)
        if result:
            return User(*result)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            db.create_user(username, pw_hash)
            flash('Bruker registrert! Logg inn.')
            return redirect(url_for('login'))
        except:
            flash('Brukernavn er allerede i bruk.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Feil brukernavn eller passord.')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    events = db.get_events_for_user(current_user.id)
    return render_template('dashboard.html', events=events, username=current_user.username)

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    title = request.form['title']
    event_date = request.form['event_date']
    event_time = request.form['event_time']
    description = request.form['description']
    db.add_event(current_user.id, title, event_date, event_time, description)
    flash('Hendelse lagt til!')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)