from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from config import BASE_LINK, STORAGE_TYPE
import json
from storage import FileStorage, MongoStorage
from parser import AdvertisementPageParser


class CrawlerBase(ABC):
    """
        class Base
    """

    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStorage()
        return FileStorage()

    @abstractmethod
    def start(self, store=False):
        """Saving automatically was not fun, so I added a parameter called store , False to True save if necessary."""
        """
        for start scripts
        """
        pass

    @abstractmethod
    def store(self, data, filename=None):
        pass

    @staticmethod
    def get(link):
        """Because we need this method in both classes"""
        try:
            response = requests.get(link)
        except requests.HTTPError:
            return None
        return response


class LinkCrawler(CrawlerBase):
    """
        for Crawl all links in page main
    """

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link
        super().__init__()

    # def get_page(self, url, start=0):
    #     try:
    #         response = requests.get(url + str(start))
    #     except:
    #         return None
    #     return response

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.find_all('a', attrs={'class': 'hdrlnk'})

    def start_crawl_city(self, url):
        start = 0
        crawl = True
        list_link_house = list()
        while crawl:
            response = self.get(url + str(start))  # We did the division ourselves
            if response is None:
                crawl = False
                continue
            new_links = self.find_links(response.text)
            list_link_house.extend(new_links)
            start += 120
            crawl = bool(len(new_links))
        return list_link_house

    def start(self, store=False):
        adv_links = list()
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            print(f'{city}total: ', len(links))
            adv_links.extend(links)
        """It is better to write the following line of code in a separate method"""
        if store:
            self.store(
                [{'url': li.get('href'), 'flag': False} for li in adv_links])  # if not written = error Serialized
        return adv_links

    def store(self, data, *args):
        # به این دلیل filename رو *args گذاشتم که اختباری باشد وارد کردن آن!!
        self.storage.store(data, 'advertisements_links')


class DataCrawler(CrawlerBase):
    """
        for crawl detail(description,id,price,...) in page detail
    """

    def __init__(self):
        super().__init__()  # اینیت صدا زدم تا از استوریج یک instance داشته باشیم تا بر روی آن __load_link را call کنیم
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()  # Composite

    def __load_links(self):
        return self.storage.load()

    def start(self, store=False):
        for link in self.links:
            response = self.get(link['url'])
            data_dict = self.parser.parse(response.text)
            if store:
                # اگر post_id نداشتی یه sample به عنوان نام فایل بذار
                # البته که میتونم مثلا از لینکه یه اسم رندوم بسازیم
                self.store(data_dict, data_dict.get('post_id', 'sample'))
            self.storage.update_flag(link)

    def store(self, data, *args):
        # دقت کنید اینجا چون لینک های صفحه جزییات کرال میشوند filename نباید null باشند
        self.storage.store(data, 'advertisement_data')
