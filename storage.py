import json
from abc import ABC, abstractmethod


class StorageBase(ABC):
    # دیزاین پترن ابسترکت
    @abstractmethod
    def store(self, data, *args):  # *args => for get Collection or filename
        pass


# اسم پترن زیر استراتژی هست چرا که crawl.py متد store نمیدونه کجا عمل سیو داره انجام میشه
# مثال : درگاه پرداخت که باید با همه به یک شکل انجام بشه
class MongoStorage(StorageBase):
    def store(self, data, *args):
        raise NotImplementedError()


class FileStorage(StorageBase):
    def store(self, data, filename, *args):
        with open(f'data/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'data/{filename}.json')  # برای بفهمم ذخیره شده
