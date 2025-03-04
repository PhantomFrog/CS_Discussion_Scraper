import requests
from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys
import csv
from autoscraper import AutoScraper

# URL of the Steam group
base_url = 'https://steamcommunity.com/groups/csgo-ts/discussions'

# Keywords to search for
keywords = ["Knife", "Bayonet"]

# Number of pages to scrape
num_pages = 3

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

# Initialize AutoScraper
scraper = AutoScraper()

# Define the example of what you want to extract
example = ["Knife"]

# Build the scraper
scraper.build(base_url, example)

filtered_topics = []

for page in range(1, num_pages + 1):
    url = f"{base_url}?p={page}"
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all discussion topics
    topics = soup.find_all('div', class_='forum_topic')

    # Get the results
    results = scraper.get_result_similar(url, unique=True)

    # Filter topics containing any of the keywords in the post content
    for topic in topics:
        post_url = topic.find('a', class_='forum_topic_overlay')['href']
        post_response = requests.get(post_url)
        post_soup = BeautifulSoup(post_response.text, 'html.parser')
        post_content = post_soup.find('div', class_='forum_op').text
        if any(keyword in post_content for keyword in keywords):
            filtered_topics.append((post_url, post_content))

# Stop the loading animation
done = True
t.join()

# Export the filtered topics to a CSV file
with open('filtered_topics.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Content'])
    for topic in filtered_topics:
        writer.writerow(topic)

# Print the filtered topics
for topic in filtered_topics:
    print(topic)