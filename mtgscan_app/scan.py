from . import azure, rec


def scan(image):
    box_texts = azure.image_to_box_texts(image)
    deck = rec.box_texts_to_deck(box_texts)
    return deck
