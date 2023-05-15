# tests/test_google_search.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import google_search

def test_google_search():
    result = google_search.google_search("Python programming")
    assert isinstance(result, str)
