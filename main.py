import requests
from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys
from autoscraper import AutoScraper

# URL of the Steam group
url = 'https://steamcommunity.com/groups/csgo-ts/discussions'

# Loading animation
done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rLoading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     \n')

t = threading.Thread(target=animate)
t.start()

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all discussion topics
topics = soup.find_all('div', class_='forum_topic')

# Initialize AutoScraper
scraper = AutoScraper()

# Define the example of what you want to extract
example = ["Bayonet"]

# Build the scraper
scraper.build(url, example)

# Get the results
results = scraper.get_result_similar(url, unique=True)

# Filter topics containing the word "Bayonet" in the post content
filtered_topics = []
for topic in topics:
    post_url = topic.find('a', class_='forum_topic_overlay')['href']
    post_response = requests.get(post_url)
    post_soup = BeautifulSoup(post_response.text, 'html.parser')
    post_content = post_soup.find('div', class_='forum_op').text
    if 'Bayonet' in post_content:
        filtered_topics.append(post_content)

# Stop the loading animation
done = True
t.join()

# Print the filtered topics
for topic in filtered_topics:
    print(topic)