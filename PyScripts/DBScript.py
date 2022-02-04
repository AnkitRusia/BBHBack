import json
from typing import Type
import certifi
from pymongo import MongoClient

client = MongoClient("mongodb+srv://bhilaibiryanihouseweb:BhilaiBiryaniHouse2022@cluster0.48fot.mongodb.net/items?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client.BBH

category_collection = db["categoryCollection"]
item_collection = db["itemCollection"]
order_collection = db["orderCollection"]
order_data_collection = db["orderDataCollection"]
expire_collection = db["expireCollection"]


print("done")
