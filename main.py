from autoscraper import AutoScraper

url = 'https://steamcommunity.com/groups/csgo-ts'

# We can add one or multiple candidates here.
# You can also put urls here to retrieve urls.
wanted_list = ["Knife"]
scraper = AutoScraper()
result = scraper.build(url, wanted_list)
print(result)