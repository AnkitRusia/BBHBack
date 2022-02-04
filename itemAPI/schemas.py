def item_serializer(item):
    return {
        "_id": str(item["_id"]),
        "name": str(item["name"]),
        "category": str(item["category"]),
        "price": [int(p) for p in item["price"]],
        "veg": int(item["veg"])
    }

def items_serializer(items):
    return [item_serializer(item) for item in items]

def category_serializer(category_dict):
    return {
        "_id": 1,
        "number": int(category_dict["number"]),
        "category": [str(c) for c in category_dict["category"]]
    }
