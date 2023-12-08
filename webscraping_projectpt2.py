from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import random
from operator import itemgetter
from plotly.graph_objs import Bar
from plotly import offline

all_quotes = []
all_tags = []

for page_num in range(1, 11):
    url = f'http://quotes.toscrape.com/page/{page_num}/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    quotes = soup.find_all('div', class_='quote')
    tags = [tag.get('content') for tag in soup.find_all('meta', class_='keywords')]

    all_quotes.extend(quotes)
    all_tags.extend(tags)


author_counts = {}
for quote in all_quotes:
    author = quote.find('small', class_='author').text
    if author in author_counts:
        author_counts[author] += 1
    else:
        author_counts[author] = 1


quote_lengths = [len(quote.find('span', class_='text').text) for quote in all_quotes]
average_quote_length = sum(quote_lengths) / len(quote_lengths)
longest_quote_index = quote_lengths.index(max(quote_lengths))
shortest_quote_index = quote_lengths.index(min(quote_lengths))
longest_quote = all_quotes[longest_quote_index].find('span', class_='text').text
shortest_quote = all_quotes[shortest_quote_index].find('span', class_='text').text


tag_counts = {}
for tag in all_tags:
    if tag in tag_counts:
        tag_counts[tag] += 1
    else:
        tag_counts[tag] = 1


sorted_authors = sorted(author_counts.items(), reverse=True, key=itemgetter(1))[:10]
top_authors = dict(sorted_authors)

print("List of all authors and the number of quotes they had:")
for author, count in sorted_authors:
    print(f"{author} - {count} quotes")

# Visualization of the top 10 tags based on popularity
sorted_tags = sorted(tag_counts.items(), reverse=True, key=itemgetter(1))[:10]
top_tags = dict(sorted_tags)

# Print analysis results
print(f"Author with the most quotes: {sorted_authors[0][0]} - {sorted_authors[0][1]} quotes")
print(f"Author with the least quotes: {sorted_authors[-1][0]} - {sorted_authors[-1][1]} quotes")
print(f"Average length of quotes: {average_quote_length:.2f} characters")
print(f"Longest quote:\n{longest_quote}")
print(f"Shortest quote:\n{shortest_quote}")
print(f"Most popular tag: {sorted_tags[0][0]}")
print(f"How many total tags were used across all quotes: {len(all_tags)}")

data = [
    {
        "type": "bar",
        "x": [author[0] for author in sorted_authors],
        "y": [author[1] for author in sorted_authors],
        "marker": {
            "color": "rgb(60,100,150)",
            "line": {"width": 1.5, "color": "rgb(25,25,25)"},
        },
        "opacity": 0.6,
    }
]

my_layout = {
    "title": "Authors with the most quotes",
    "xaxis": {"title": "Authors"},
    "yaxis": {"title": "Number of Quotes"},
}

fig = {"data": data, "layout": my_layout}

offline.plot(fig, filename="authors_quotes.html")


data = [
    {
        "type": "bar",
        "x": [tag[0] for tag in sorted_tags],
        "y": [tag[1] for tag in sorted_tags],
        "marker": {
            "color": "rgb(60,100,150)",
            "line": {"width": 1.5, "color": "rgb(25,25,25)"},
        },
        "opacity": 0.6,
    }
]

my_layout = {
    "title": "Most popular tags",
    "xaxis": {"title": "Tags"},
    "yaxis": {"title": "Number of Tags"},
}

fig = {"data": data, "layout": my_layout}

offline.plot(fig, filename="top_tags.html")