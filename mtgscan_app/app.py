import os
import threading
import time
from pathlib import Path

from celery import Celery
from flask import Flask, jsonify, render_template, request, send_from_directory
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition
from werkzeug.utils import secure_filename

DIR_ROOT = Path(__file__).parents[1]
azure = Azure()
rec = None

UPLOAD_FOLDER = Path(__file__).parent / "dl"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Initialize Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100_000_000
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize Celery
celery = Celery(app.name)
celery.conf.update(CELERY_BROKER_URL='redis://localhost:6379/0',
                   CELERY_RESULT_BACKEND='redis://localhost:6379/0',
                   CELERY_TASK_SERIALIZER="pickle",
                   CELERY_ACCEPT_CONTENT=['pickle'])

def load_cards():
    global rec
    if rec is None:
        rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"),
                               file_keywords=(DIR_ROOT / "Keywords.json"),
                               max_ratio_diff=0.2)


@app.before_first_request
def init():
    thread = threading.Thread(target=load_cards)
    thread.start()


def wait_rec():  # wait until rec files are loaded
    while not rec:
        time.sleep(5)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@celery.task()
def scan():
    emit("{"deck": str("dck")}


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    scan.apply_async()
    return render_template("upload.html")


@app.route('/api/<path:url>')
def api_scan(url):
    deck = scan(url, azure, rec, None)
    return jsonify({"maindeck": deck.maindeck.cards, "sideboard": deck.sideboard.cards})
