import requests

def get_random_cat_fact():
    try:
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            data = response.json()
            return data['fact']
        else:
            return f"Failed to retrieve cat fact. Error code: {response.status_code}"
    except requests.exceptions.RequestException:
        return "Sorry, I couldn't retrieve a cat fact right now. Please try again later."
