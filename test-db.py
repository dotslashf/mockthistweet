from db_mongo import Database
import sys
sys.path.insert(0, 'db_mongo.py')


db = Database()
db.connect_db('twitter')
db.select_col('environment')

x = db.collection.find_one()
print(x)
