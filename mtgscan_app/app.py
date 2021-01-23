import os
from pathlib import Path
import threading
import time

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from pathlib import Path

from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition

from mtgscan_app.scan import scan

DIR_ROOT = Path(__file__).parents[1]
azure = Azure()
rec = None

UPLOAD_FOLDER = str(Path(__file__).parent / "dl")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100_000_000
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.before_first_request
def before_first_request():
    def load():
        """
        This function cleans up old tasks from our in-memory data structure.
        """
        global rec

        rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"),
                               file_keywords=(DIR_ROOT / "Keywords.json"),
                               max_ratio_diff=0.2)

    thread = threading.Thread(target=load)
    thread.start()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deck, filename = "", ""
    if request.method == 'POST':
        while not rec:
            time.sleep(5)
        path = None
        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(path)
        elif "url_image" in request.form and request.form["url_image"]:
            path = request.form["url_image"]
        if path:
            filename = "image.png"
            deck = scan(path, os.path.join(app.config['UPLOAD_FOLDER'], filename), azure, rec)
    return render_template("upload.html", deck=deck, image=filename)
