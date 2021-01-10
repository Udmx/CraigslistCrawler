import sys

from crawl import LinkCrawler, DataCrawler
from config import CITIES

# def get_page(url, start=0):
#     try:
#         response = requests.get(url + str(start))
#     except:
#         return None
#     print(response.status_code, response.url)
#     return response
#
#
# def find_links(html_doc):
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     return soup.find_all('a', attrs={'class': 'hdrlnk'})
#
#
# def start_crawl_city(url):
#     start = 0
#     crawl = True
#     list_link_house = list()
#     while crawl:
#         response = get_page(url, start)
#         if response is None:
#             crawl = False
#             continue
#         new_links = find_links(response.text)
#         list_link_house.extend(new_links)
#         start += 120
#         crawl = bool(len(new_links))
#     return list_link_house
#
#
# def start_crawl():
#     cities = ['london', 'paris', 'losangeles']
#     link = 'https://{}.craigslist.org/search/hhh?availabilityMode=0&lang=en&cc=gb&s='
#     for city in cities:
#         links = start_crawl_city(link.format(city))
#         print(f'{city}total: ', len(links))

#
# def get_pages_data():
#     raise NotImplementedError()


if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == 'find_links':
        crawler = LinkCrawler(cities=CITIES)
        crawler.start(store=True)
    elif switch == 'extract_pages':
        crawler = DataCrawler()
        crawler.start(store=True)
