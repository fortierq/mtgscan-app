import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from mtgscan_app.scan import scan

UPLOAD_FOLDER = '/home/qfortier/Code/mtgscan-app/mtgscan_app/dl/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# default value during development
# app.secret_key = b'\xff(\x13\x96\xa7U\xb2\x14B\tZ\x0em\xaa\xc7\x08'
# overridden if this file exists in the instance folder
# app.config.from_pyfile('config.py', silent=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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