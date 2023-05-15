# MIT License

# Copyright (c) 2023 - Jeremy Stevens

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import wikipedia
from tqdm import tqdm
import time

"""
This module contains a function to fetch a summary from Wikipedia.

The function uses the Wikipedia API.

Functions:
wikipedia_search: Fetches a summary from Wikipedia.
"""

def handle_wikipedia_search(query):
    """
        Fetches a summary from Wikipedia.

        Args:
        query (str): Search query.

        Returns:
        str: A string containing the Wikipedia summary, or an error message.
        """
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Wikipedia"):
        time.sleep(0.01)
    results = wikipedia.summary(query)
    return results
