import os
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
DATA = ROOT / 'data'
COMMENTS = DATA / 'comments'
COMMENTS_CSV = DATA / 'comments.csv'

