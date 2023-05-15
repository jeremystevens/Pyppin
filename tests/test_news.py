# tests/test_news.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import fetch_news

def test_fetch_news():
    result = fetch_news.fetch_news("Python programming")
    assert isinstance(result, str)
