import os
from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

from mtgscan_app.scan import scan

UPLOAD_FOLDER = str(Path(__file__).parent / "dl")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100_000_000
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deck, filename = "", ""
    if request.method == 'POST':
        path = None
        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
        elif "url_image" in request.form and request.form["url_image"]:
            path = request.form["url_image"]
        if path:
            filename = "image.png"
            deck = scan(path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("upload.html", deck=deck, image=filename)
