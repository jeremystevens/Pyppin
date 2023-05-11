from googlesearch import search
from tqdm import tqdm
import time

def handle_google_search():
    query = input("What would you like to search for: ")
    search_results = []
    # Show progress bar
    for _ in tqdm(range(100), desc="Searching Google"):
        time.sleep(0.01)
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        search_results.append(j)

    return "\n".join(search_results)
