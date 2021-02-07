import eventlet
eventlet.monkey_patch()

import os
from pathlib import Path

from celery import Celery
from flask import Flask, jsonify, render_template
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition
from flask_socketio import SocketIO

DIR_ROOT = Path(__file__).parents[1]
REDIS_URL = "redis://localhost:6379/0"

# Initialize Flask, SocketIO, Celery
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

socketio = SocketIO(app, message_queue=REDIS_URL)

celery = Celery(app.name)
celery.conf.update(CELERY_BROKER_URL=REDIS_URL, CELERY_RESULT_BACKEND=REDIS_URL)

@app.route("/")
def index():
    return render_template("upload.html")

@socketio.on("scan")
def scan_io(msg):
    scan_celery.apply_async((msg["image"],))

@celery.task
def scan_celery(image):
    deck = scan(image)
    sio = SocketIO(message_queue=REDIS_URL)
    sio.emit("scan_result", {"deck": deck.maindeck.cards, "image": ""})

def scan(image):
    rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"),
                           file_keywords=(DIR_ROOT / "Keywords.json"),
                           max_ratio_diff=0.2)
    azure = Azure()
    box_texts = azure.image_to_box_texts(image)
    box_cards = rec.box_texts_to_cards(box_texts)
    rec.assign_stacked(box_texts, box_cards)
    box_cards.save_image(image, "image.png")
    deck = rec.box_texts_to_deck(box_texts)
    return deck

@app.route("/api/<path:url>")
def api_scan(url):
    deck = scan(url)
    return jsonify({"maindeck": deck.maindeck.cards, "sideboard": deck.sideboard.cards})

if __name__ == "__main__":
    socketio.run(app, debug=True)
