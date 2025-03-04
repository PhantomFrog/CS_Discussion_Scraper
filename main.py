import requests
from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys
import csv
from autoscraper import AutoScraper

# URL of the Steam group, must be discussions page
base_url = 'https://steamcommunity.com/groups/Example/discussions'

# General keywords to search for
general_keywords = ["Knife"]

# Number of pages to scrape
num_pages = 50

# Loading animation
done = False
current_page = 1

def animate():
    global current_page
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write(f'\rLoading page {current_page} ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     \n')

t = threading.Thread(target=animate)
t.start()

# Initialize AutoScraper
scraper = AutoScraper()

# Define the wanted list based on general keywords
wanted_list = general_keywords

# Build the scraper
scraper.build(base_url, wanted_list=wanted_list)

filtered_topics = []
seen_urls = set()

for page in range(1, num_pages + 1):
    current_page = page
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

    # Filter topics containing any of the general keywords in the post content
    for topic in topics:
        post_url = topic.find('a', class_='forum_topic_overlay')['href']
        if post_url not in seen_urls:
            post_response = requests.get(post_url)
            post_soup = BeautifulSoup(post_response.text, 'html.parser')
            post_content = post_soup.find('div', class_='forum_op').text.lower()
            found_keywords = [keyword for keyword in general_keywords if keyword.lower() in post_content]
            if found_keywords:
                filtered_topics.append((post_url, ', '.join(found_keywords)))
                seen_urls.add(post_url)

# Stop the loading animation
done = True
t.join()

# Export the filtered topics to a CSV file
with open('filtered_topics.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Keywords Found'])
    for topic in filtered_topics:
        writer.writerow(topic)

