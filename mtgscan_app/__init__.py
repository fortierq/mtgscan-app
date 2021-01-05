__version__ = '0.1.0'

from pathlib import Path

import mtgscan
from mtgscan.ocr import Azure
from mtgscan.text import MagicRecognition

DIR_ROOT = Path(__file__).parents[1]

azure = Azure()
rec = MagicRecognition(file_all_cards=str(DIR_ROOT / "all_cards.txt"), 
                       file_keywords=(DIR_ROOT / "Keywords.json"))