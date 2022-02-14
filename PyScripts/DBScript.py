import json
from typing import Type
import certifi
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://bhilaibiryanihouseweb:BhilaiBiryaniHouse2022@cluster0.48fot.mongodb.net/items?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client.BBH

category_collection = db["categoryCollection"]
item_collection = db["itemCollection"]
order_collection = db["orderCollection"]
order_data_collection = db["orderDataCollection"]
expire_collection = db["expireCollection"]


print("done")

def order_serializer(order):
    return {
        "_id": int(order["_id"]),
        "date": datetime,
        "items": itemqty_serializer(order["items"]),
        "amount": int,
        "ordernumber": int,
        "tablenumber": int
    }

def all_order_serializer(orders):
    return [order_serializer(order) for order in orders]

op = order_collection.find()
all_order_serializer(op)
