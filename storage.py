import json
from abc import ABC, abstractmethod
from mongo import MongoDatabase


class StorageBase(ABC):
    # دیزاین پترن ابسترکت
    @abstractmethod
    def store(self, data, *args):  # *args => for get Collection or filename
        pass

    @abstractmethod
    def load(self):
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

    def load(self):
        return self.mongo.database.advertisements_links.find({'flag': False})

    def update_flag(self, data):
        """پس از ذخیره سازی این متد میاد و flag رو برابر True قرار میدهد تا ما دوباره crawl نکنیم"""
        self.mongo.database.advertisements_links.find_one_and_update(
            {'_id': data['_id']},
            {'$set': {'flag': True}}
        )


class FileStorage(StorageBase):
    def store(self, data, *args):
        filename = args[0] + '-' + data['post_id']
        with open(f'data/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'data/{filename}.json')  # برای بفهمم ذخیره شده

    def load(self):
        with open('data/advertisement_data.json', 'r') as f:
            links = json.loads(f.read())
            return links

    def update_flag(self):
        """ این متد نوشتیم تا خطا در صورت نوع ذخیره سازی فایل به وجود نیاد و البته کاری لازم نیست بکنه"""
        pass
