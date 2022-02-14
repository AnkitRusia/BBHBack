from datetime import datetime

def itemqty_serializer(item):
    return {
        "_id": str(item["_id"]),
        "name": str(item["name"]),
        "category": str(item["category"]),
        "price": [int(p) for p in item["price"]],
        "veg": int(item["veg"]),
        "qty": int(item["qty"])
    }

def getitems__serializer(getitem):
    return {
        "amount": int(getitem["amount"]),
        "items": [itemqty_serializer(itemqty) for itemqty in getitem["items"]]
    }

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
    def one_order_serializer(order):
        return dict(order)
    
    all_orders = [one_order_serializer(order) for order in orders]
    return all_orders
