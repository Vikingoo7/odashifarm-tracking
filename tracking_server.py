from flask import Flask, request, send_file, render_template_string, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import os

app = Flask(__name__)

# Connect to database file (TinyDB will create if not exists)
db = TinyDB('opens_db.json')

# Route for tracking pixel
@app.route('/track')
def track():
    email = request.args.get('email')
    if email:
        db.insert({
            'email': email,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })
        print(f"New open recorded: {email} at {datetime.utcnow()}")
    return send_file('pixel.png', mimetype='image/png')

# Simple dashboard (we'll protect it soon!)
@app.route('/dashboard')
def dashboard():
    opens = db.all()
    opens_html = "<h1>Opens Dashboard</h1><table border='1'><tr><th>Email</th><th>Timestamp</th></tr>"
    for open_event in opens:
        opens_html += f"<tr><td>{open_event['email']}</td><td>{open_event['timestamp']}</td></tr>"
    opens_html += "</table>"
    return opens_html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)