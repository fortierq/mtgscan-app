import os
import time
from pathlib import Path

from celery import Celery
from flask import Flask, jsonify, render_template, request, send_from_directory
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition
from werkzeug.utils import secure_filename

from .scan import scan

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
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def load_cards():
    return {
        "cards":
        MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"),
                         file_keywords=(DIR_ROOT / "Keywords.json"),
                         max_ratio_diff=0.2)
    }


@app.before_first_request
def init():
    global task_load_cards
    task_load_cards = load_cards.delay()


def wait_rec():  # wait until rec files are loaded
    global rec
    result = load_cards.AsyncResult(task_load_cards.id)
    while not rec and result.state == "PENDING":
        time.sleep(5)
    rec = task_load_cards.info.get("cards", None)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deck, filename = "", ""
    if request.method == 'POST':
        wait_rec()
        image = None
        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            image = app.config['UPLOAD_FOLDER'] / filename
            file.save(image)
        elif "url_image" in request.form and request.form["url_image"]:
            image = request.form["url_image"]
        if image:
            filename = "image.png"
            deck = scan(image, azure, rec, app.config['UPLOAD_FOLDER'] / filename)
    return render_template("upload.html", deck=deck, image=filename)


@app.route('/api/<path:url>')
def api_scan(url):
    wait_rec()
    deck = scan(url, azure, rec, None)
    return jsonify({"maindeck": deck.maindeck.cards, "sideboard": deck.sideboard.cards})
