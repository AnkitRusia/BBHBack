from pymongo import MongoClient
from decouple import config

mongouri = config('MONGO_DETAILS')
client = MongoClient(mongouri)
db = client.BBH

category_collection = db["categoryCollection"]
item_collection = db["itemCollection"]
order_collection = db["orderCollection"]
order_data_collection = db["orderDataCollection"]
expire_collection = db["expireCollection"]
user_collection = db["userCollection"]

