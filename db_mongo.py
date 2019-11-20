import pymongo


class Database:
    def __init__(self, database, collection):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[database]
        self.col = self.db[collection]
        self.last_id = None

    def find_last_object(self):
        list_col = self.col.find().sort('_id', -1)

        for i, t in enumerate(list_col):
            if i == 0:
                last_tweet_id = t['tweet_last_id']
                last_id = t['_id']
                last = {'last_id': last_id, 'last_tweet_id': last_tweet_id}

        self.last_id = last['last_id']
        return last

    def insert_object(self, tweet):
        l_id = self.last_id + 1
        data = {'_id': l_id, 'tweet_last_id': tweet}

        self.col.insert_one(data)
