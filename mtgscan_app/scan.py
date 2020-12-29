from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition


def scan(image):
    azure = Azure()
    rec = MagicRecognition()
    box_texts = azure.image_to_box_texts(image)
    deck = rec.box_texts_to_deck(box_texts)
    return deck
