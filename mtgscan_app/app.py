import os
from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

from mtgscan_app.scan import scan

UPLOAD_FOLDER = str(Path(__file__).parent / "dl")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100_000_000
app.secret_key = b'\xff(\x13\x96\xa7U\xb2\x14B\tZ\x0em\xaa\xc7\x08'

import sys
from pathlib import Path

import mtgscan
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition

DIR_ROOT = Path(__file__).parents[1]

azure = Azure()
rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"), 
                       file_keywords=(DIR_ROOT / "Keywords.json"))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deck, filename = "", ""
    print(os.listdir("."))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            deck = scan(path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("upload.html", deck=deck, image=filename)
