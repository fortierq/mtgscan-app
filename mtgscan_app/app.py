import time

from flask import render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

from mtgscan_app import app, azure, rec


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
            path = app.config['UPLOAD_FOLDER'] / filename
            file.save(path)
        elif "url_image" in request.form and request.form["url_image"]:
            path = request.form["url_image"]
        if path:
            filename = "image.png"
            deck = scan(path, app.config['UPLOAD_FOLDER'] / filename, azure, rec)
    return render_template("upload.html", deck=deck, image=filename)

@app.route('/api/<path:url>')
def api(url):
    deck = scan(url, None, azure, rec)
    return jsonify(deck.maindeck)