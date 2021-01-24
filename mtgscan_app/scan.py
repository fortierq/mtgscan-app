

def scan(image, azure, rec, output_image=None):
    box_texts = azure.image_to_box_texts(image)
    box_cards = rec.box_texts_to_cards(box_texts)
    rec.assign_stacked(box_texts, box_cards)
    if output_image:
        box_cards.save_image(image, output_image)
    deck = rec.box_texts_to_deck(box_texts)
    return deck
