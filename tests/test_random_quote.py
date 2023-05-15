# tests/test_random_quote.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import random_quote

def test_random_quote():
    result = random_quote.get_random_quote()
    assert isinstance(result, str)
