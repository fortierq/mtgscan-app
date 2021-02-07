import eventlet
eventlet.monkey_patch()

import os
import threading
import time
from pathlib import Path

from celery import Celery
from flask import Flask, jsonify, render_template, request, send_from_directory
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit

DIR_ROOT = Path(__file__).parents[1]
azure = Azure()
rec = None

UPLOAD_FOLDER = Path(__file__).parent / "dl"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize Flask
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100_000_000
app.secret_key = os.environ.get("SECRET_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

socketio = SocketIO(app, message_queue="redis://localhost:6379/0")

# Initialize Celery
celery = Celery(app.name)
celery.conf.update(CELERY_BROKER_URL="redis://localhost:6379/0",
                   CELERY_RESULT_BACKEND="redis://localhost:6379/0",
                   CELERY_TASK_SERIALIZER="pickle",
                   CELERY_ACCEPT_CONTENT=["pickle", "json"])

@app.route("/")
def index():
    return render_template("upload.html")

@socketio.on("scan")
def start_scan(msg):
    print("bla")
    scan.apply_async((msg["image"],))

@celery.task
def scan(image):
    rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"),
                           file_keywords=(DIR_ROOT / "Keywords.json"),
                           max_ratio_diff=0.2)
    box_texts = azure.image_to_box_texts(image)
    box_cards = rec.box_texts_to_cards(box_texts)
    rec.assign_stacked(box_texts, box_cards)
    box_cards.save_image(image, "image.png")
    deck = rec.box_texts_to_deck(box_texts)

    sio = SocketIO(message_queue="redis://localhost:6379/0")
    sio.emit("scan_result", {"deck": deck.maindeck.cards, "image": "image.png"})

@app.route("/api/<path:url>")
def api_scan(url):
    deck = scan(url, azure, rec, None)
    return jsonify({"maindeck": deck.maindeck.cards, "sideboard": deck.sideboard.cards})

if __name__ == "__main__":
    socketio.run(app, debug=True)
