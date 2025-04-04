from flask import Flask, request, send_file
from datetime import datetime

app = Flask(__name__)

# Folder where we save logs
LOG_FILE = "opens_log.txt"

@app.route('/track', methods=['GET'])
def track_email_open():
    # Get customer's email from URL parameter
    email = request.args.get('email', 'unknown')

    # Save the open event with timestamp
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {email} opened the email.\n")

    # Return a 1x1 transparent pixel
    return send_file('pixel.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)