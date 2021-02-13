import eventlet
eventlet.monkey_patch()

import os
from pathlib import Path

from celery import Celery, Task
from flask import Flask, jsonify, render_template
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition
from flask_socketio import SocketIO

DIR_DATA = Path(__file__).parent / "data"
REDIS_URL = "redis://redis:6379/0"
# REDIS_URL = "redis://localhost:6379/0"

# Initialize Flask, SocketIO, Celery
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

socketio = SocketIO(app, message_queue=REDIS_URL)

celery = Celery(app.name, broker=REDIS_URL, backend=REDIS_URL)


class ScanTask(Task):
    def __init__(self):
        self._rec = MagicRecognition(file_all_cards=str(DIR_DATA / "all_cards.txt"),
                                     file_keywords=(DIR_DATA / "Keywords.json"),
                                     max_ratio_diff=0.2)


@app.route("/")
def index():
    return render_template("upload.html")


@socketio.on("scan")
def scan_io(msg):
    scan_celery.apply_async((msg["image"], ))


@celery.task(base=ScanTask)
def scan_celery(image):
    deck = scan(scan_celery._rec, image)
    sio = SocketIO(message_queue=REDIS_URL)
    sio.emit("scan_result", {"deck": deck.maindeck.cards, "image": ""})


def scan(rec, image):
    azure = Azure()
    box_texts = azure.image_to_box_texts(image)
    box_cards = rec.box_texts_to_cards(box_texts)
    rec.assign_stacked(box_texts, box_cards)
    box_cards.save_image(image, "image.png")
    deck = rec.box_texts_to_deck(box_texts)
    return deck


@app.route("/api/<path:url>")
def api_scan(url):
    rec = MagicRecognition(file_all_cards=str(DIR_DATA / "all_cards.txt"),
                           file_keywords=(DIR_DATA / "Keywords.json"),
                           max_ratio_diff=0.2)
    deck = scan(rec, url)
    return jsonify({"maindeck": deck.maindeck.cards, "sideboard": deck.sideboard.cards})


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
    # socketio.run(app, debug=True)
