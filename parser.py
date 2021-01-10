from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            return title_tag.text
        # If I do not leave else, it returns None

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.text

    @property
    def body(self):
        body_tag = self.soup.select_one('#postingbody')
        if body_tag:
            return body_tag.text

    @property
    def post_id(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(1)'
        post_id_tag = self.soup.select_one(selector)
        if post_id_tag:
            # Note : Replace 'post id : 5454848' to '54544848'
            return post_id_tag.text.replace('post id: ', '')

    @property
    def created_time(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(2) > time'
        created_time_tag = self.soup.select_one(selector)
        if created_time_tag:
            return created_time_tag.attrs['datetime']

    @property
    def modified_time(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(3) > time'
        modified_time_tag = self.soup.select_one(selector)
        if modified_time_tag:
            return modified_time_tag.attrs['datetime']

    def parse(self, html_data):
        self.soup = BeautifulSoup(html_data, 'html.parser')
        """I created a dictionary to store data that could be converted to Json"""
        data = {'title': self.title, 'price': self.price, 'body': self.body, 'post_id': self.post_id,
                'created_time': self.created_time,
                'modified_time': self.modified_time}
        return data
