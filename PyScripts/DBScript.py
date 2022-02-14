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

def capname(name):
    ns = name.split(" ")
    new_name = ''
    new_id = ''
    for word in ns:
        new_name += word[0].upper() + word[1:] + " "
        new_id += word[0].upper() + word[1:] + "_"
    new_id = new_id[:-1]
    return new_name, new_id


# items ke name ka 1st capital
all_name = item_collection.find()
for name in all_name:
    name = dict(name)
    cat = name["category"]
    if cat == "biryani":
        name["category"] = "Biryani"
    item_collection.find_one_and_update({"_id": name["_id"]}, {"$set": name})
print("Done")



# delete kutta