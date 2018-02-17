# import libraries
import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

headlines = []
links = []
# specify the url
quote_page = 'http://www.spox.com/de/sport/ussport/nba/index.html'
# print(quote_page)

# query the website and return the html to the variable 'page'
page = urllib.request.urlopen(quote_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# get all elements under class='ct'
#price_box = soup.find('div', attrs={'class': 'ct'})
price_box = soup.find_all('div', attrs={'class': lambda L: L and L.startswith('itm txinpic i')})

# get all div with headlines
h_result = []
for p in price_box:
    h_result.extend(p.find_all('div'))
# append all headlines to list
for h in h_result:
    if h.find('h2') is not None:
        headlines.append(h.find('h2').text)

# get all a with links
l_result = []
for p in price_box:
    l_result.extend(p.find_all('a', attrs={'class': 'lnk'}))
# append all links to list
for l in l_result:
    if l.get('href') is not None:
        links.append(l.get('href'))

# save the data in tuple
d_news = {}
d_news = dict(zip(headlines, links))

# open a csv file with append, so old data will not be erased
path = '/Users/peterhartmann/Documents/Python/scraping/'
with open(os.path.join(path, 'nba_scrape_' + datetime.now().strftime('%y%m%d%H%M%S') + '.csv'), "w", encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=';', quotechar='|')
    # The for loop
    for d in d_news:
        writer.writerow([d, d_news[d], datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        #print(d)
