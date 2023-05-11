import wikipedia
from tqdm import tqdm
import time

def handle_wikipedia_search():
    search_query = input("What would you like to search for: ")
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Wikipedia"):
        time.sleep(0.01)
    results = wikipedia.summary(search_query)
    return results
