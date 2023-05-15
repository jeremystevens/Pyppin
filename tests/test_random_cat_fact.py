# tests/test_random_cat_fact.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import random_cat_fact

def test_random_cat_fact():
    result = random_cat_fact.get_random_cat_fact()
    assert isinstance(result, str)
