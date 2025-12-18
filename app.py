from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        event_date = request.form['event_date']
        event_time = request.form['event_time'] or None
        description = request.form['description']
        db.add_event(title, event_date, event_time, description)
        return redirect('/')
    events = db.get_events()
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)