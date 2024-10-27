import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://example.com'

try:
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title tag's content
    title = soup.title.string if soup.title else 'No title found'
    print(f'Title of the page: {title}')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
