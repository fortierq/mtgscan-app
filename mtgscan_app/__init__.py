import os
import threading
from pathlib import Path

from flask import Flask
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition

print(1)

DIR_ROOT = Path(__file__).parents[1]
azure = Azure()
rec = None

UPLOAD_FOLDER = DIR_ROOT / "dl"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100_000_000
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Load cards
def load():
    global rec

    rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"),
                           file_keywords=(DIR_ROOT / "Keywords.json"),
                           max_ratio_diff=0.2)


if not rec:
    thread = threading.Thread(target=load)
    thread.start()
