import json
from abc import ABC, abstractmethod
from mongo import MongoDatabase


class StorageBase(ABC):
    # دیزاین پترن ابسترکت
    @abstractmethod
    def store(self, data, *args):  # *args => for get Collection or filename
        pass


# اسم پترن زیر استراتژی هست چرا که crawl.py متد store نمیدونه کجا عمل سیو داره انجام میشه
# مثال : درگاه پرداخت که باید با همه به یک شکل انجام بشه
class MongoStorage(StorageBase):
    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, *args):
        collection = getattr(self.mongo.database, args[0])
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)  # همه را به یکباره ذخیره کن
        else:
            collection.insert_one(data)  # دونه دونه ذخیره میکنی در یک کالکشن


class FileStorage(StorageBase):
    def store(self, data, *args):
        filename = args[0] + '-' + str(data['post_id'])
        with open(f'data/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'data/{filename}.json')  # برای بفهمم ذخیره شده
