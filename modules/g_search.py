from googlesearch import Search

def handle_google_search(query):
    try:
        # Perform the Google search
        search_results = Search(query)
        results = search_results.results

        # Check if there are any results
        if results:
            # Extract the title and link for the top result
            top_result = results[0]
            title = top_result.title
            link = top_result.url
            return f"Title: {title}\nLink: {link}"
        else:
            return "No results found."
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage:
#query = input("Ask me something: ")
#result = google_search_top_result(query)
#print(result)
