# tests/test_wikipedia_search.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import wikipedia_search

def test_wikipedia_search():
    result = wikipedia_search.wikipedia_search("Python programming")
    assert isinstance(result, str)
