import os
import sys
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from mtgscan_app.scan import scan

UPLOAD_FOLDER = str(Path(__file__).parent / "dl")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# default value during development
# app.secret_key = b'\xff(\x13\x96\xa7U\xb2\x14B\tZ\x0em\xaa\xc7\x08'
# overridden if this file exists in the instance folder
# app.config.from_pyfile('config.py', silent=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100_000_000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deck = "no deck"
    if request.method == 'POST':    
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            print(file)
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            deck = scan(path)
            return render_template("upload.html", deck=deck)
    return render_template("upload.html", deck=deck)
