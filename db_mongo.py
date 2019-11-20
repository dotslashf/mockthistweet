import pymongo


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = None
        self.collection = None

    def connect_db(self, database):
        try:
            db_list = self.client.list_database_names()
            if database in db_list:
                print('connected to {}'.format(database))
                self.db = self.client[database]
            else:
                print('no database such as {} found'.format(database))

        except Exception as e:
            print(e)

    def select_col(self, collection):
        try:
            col_list = self.db.list_collection_names()
            if collection in col_list:
                self.collection = self.db[collection]
            else:
                print('no collection such as {} found'.format(collection))
        except Exception as e:
            print(e)

    def find_last_object(self):
        if self.collection is not None:
            list_col = self.collection.find().sort('_id', -1)

            for i, t in enumerate(list_col):
                if i == 0:
                    last = t
                    return last
        else:
            print('Please connect first')

    def insert_object(self, data):
        last = self.find_last_object()
        last_id = last['_id'] + 1

        data.update({'_id': last_id})

        self.collection.insert_one(data)


# db = Database()
# db.connect_db('twitter')
# db.select_col('tweet')
# l = db.find_last_object()
# db.insert_object({'tweet_last_id': 1197212312232439000})
