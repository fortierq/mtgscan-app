import eventlet
eventlet.monkey_patch()

import os

from flask import Flask, render_template
from flask_socketio import SocketIO

REDIS_URL = "redis://redis:6379/0"

# Initialize Flask, SocketIO, Celery
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
socketio = SocketIO(app, message_queue=REDIS_URL, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("upload.html")


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
