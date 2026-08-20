# import
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import generate_data

def test_generate_data():
    assert generate_data.generate() == 0