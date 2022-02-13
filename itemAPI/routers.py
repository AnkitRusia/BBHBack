from fastapi import APIRouter, HTTPException, status
from itemAPI.models import Item
from itemAPI.schemas import item_serializer, items_serializer, category_serializer
from mongosetup.mongodb import category_collection, item_collection, order_collection, client
from utils.common import expired
from typing import List


router = APIRouter(
    prefix="/item",
    tags=["items"],
    responses={404: {"description": "Item not available!"}},
)



@router.get("")
def get_all_items():
    try:
        expired()
        items = item_collection.find()
        return items_serializer(items)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post('')
def add_item(items: List[Item]):
    expired()
    try:
        if len(items) == 999:
            for item in items:
                item = dict(item)
                prices = item["price"]
                price_list = []
                for _price in prices:
                    try:
                        price_list.append(int(_price))
                    except:
                        pass
                item["price"] = price_list
                item["_id"] = item["name"].replace(" ", "_")
                _id = item_collection.insert_one(dict(item))
            return {"OK": "OK", "status": 200}
        else:
            return {"status": "Can not add more than 5 items", "status": 404}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/{id}')
def get_by_id(id: str):
    expired()
    item = item_collection.find_one({"_id": id})
    if item:
        return item_serializer(item)
    else:
        return {404: "Not Found"}

@router.put('/{id}')
def update_by_id(id: str, item: Item):
    expired()
    try:
        item = dict(item)
        old_id = id
        new_id = item["name"].replace(" ", "_")
        item["_id"] = new_id
        try: 
            item_collection.find_one_and_delete({"_id": old_id})
            item_collection.find_one_and_delete({"_id": new_id})
        except Exception as e:
            pass
        prices = item["price"]
        price_list = []
        for _price in prices:
            try:
                price_list.append(int(_price))
            except:
                pass
        item["price"] = price_list
        item_collection.insert_one(item)
        new_item = item_collection.find_one({"_id": id})
        return item_serializer(new_item)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get('/category')
def get_category():
    expired()
    try:
        category = category_collection.find_one({"_id": 1})
        return category_serializer(category)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get('/category/{cat}')
def get_items_by_category(cat: str):
    expired()
    try:
        items = item_collection.find({"category": cat})
        return items_serializer(items)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
