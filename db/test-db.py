import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["twitter"]

mycol = mydb["tweet"]

mylist = [
    {'_id': 1, 'tweet_last_id': 1197112985367408640},
    {'_id': 2, 'tweet_last_id': 1197112985367408641},
    {'_id': 3, 'tweet_last_id': 1197112985367408642},
    {'_id': 4, 'tweet_last_id': 1197112985367408643},
    {'_id': 5, 'tweet_last_id': 1197112985367408644}
]

# insert = mycol.insert_many(mylist)

mydoc = mycol.find().sort('_id', -1)

for i, t in enumerate(mydoc):
    if i == 0:
        last = t['tweet_last_id']
        last = str(last)

print(last)
