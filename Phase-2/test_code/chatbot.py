import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get API key and Search Engine ID from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Function to get search results using Google Custom Search API
def google_search(query):
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": 3  # Get top 3 results
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()

        results = []
        if "items" in search_results:
            for item in search_results["items"]:
                results.append({"title": item["title"], "link": item["link"], "snippet": item["snippet"]})
        return results
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Streamlit App for Google Search Question Answer
def main():
    st.title("Google Search Question Answer Integration")
    st.write("Ask a question and I'll search Google for the best results:")

    # Input field for user question
    user_query = st.text_input("Your Question:", key="input")

    if st.button("Search"):
        if user_query:
            # Get search results
            search_results = google_search(user_query)
            if isinstance(search_results, str):
                st.error(search_results)  # Display error message if request fails
            elif len(search_results) == 0:
                st.warning("No results found.")
            else:
                # Display search results
                st.subheader("Top Results:")
                for result in search_results:
                    st.write(f"**{result['title']}**")
                    st.write(f"{result['snippet']}")
                    st.write(f"[Link]({result['link']})")
                    st.write("---")

if __name__ == "__main__":
    main()
