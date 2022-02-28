from sqlite3 import Date
from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
from ordersAPI.models import  GetItems, Stats, ConnectionManager, GetTotalOrders, PaymentMethod, Dates
from mongosetup.mongodb import order_collection, order_data_collection
from datetime import datetime
from typing import List
from utils.common import expired
from ordersAPI.schemas import all_order_serializer, order_serializer

  
router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "order not available!"}},
)

manager = ConnectionManager()
@router.websocket("/notification/{name}")
async def notify_instant(websocket: WebSocket, name: str):
    await manager.connect(websocket, name)
    while True:
        try: 
            data = await websocket.receive_text()
            await manager.broadcast(data)
        except WebSocketDisconnect:
            manager.disconnect(websocket, name)
        except:
            break
        

@router.post("/stats")
def get_stats(stats: Stats):
    stats = dict(stats)
    orders = order_data_collection.find()
    total_amount = 0
    bills = []
    for od in orders:
        try:
            if od['date'].month == stats["month"]:
                total_amount += od['amount']
                bills.append(od)
        except KeyError:
            pass
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {
        "total_amount": total_amount,
        "bills": bills
    }

@router.get("/tables")
def get_all_orders():
    try:
        all_orders = order_collection.find()
        return all_order_serializer(all_orders)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/currentOrder/{tablenumber}")
def get_order(tablenumber: int):
    expired()
    try:
        current_order = order_collection.find_one({"tablenumber": tablenumber})
        return current_order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/paid/{tablenumber}")
def delete_bill_paid(tablenumber: int, paymentMethod: PaymentMethod):
    expired()
    try:
        paymentMethod = dict(paymentMethod)
        order = order_collection.find_one({"tablenumber": tablenumber})
        max_id = order_data_collection.find_one({'$query':{},'$orderby':{'_id':-1}})["_id"]
        order["_id"] = max_id + 1
        order["tablenumber"] = str(tablenumber)
        order["paymentMethod"] = paymentMethod["paymentMethod"]
        order_data_collection.insert_one(order)
        order_collection.find_one_and_delete({"tablenumber": tablenumber})
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/del/{tablenumber}")
def delete_clear_table_lost_customer(tablenumber: int):
    try:
        order_collection.find_one_and_delete({"tablenumber": tablenumber})
        return {"status": 200}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/newOrder/{tablenumber}")
def new_order(tablenumber: int, getItems: GetTotalOrders):
    expired()
    try:
        getItems = dict(getItems)
        if order_collection.count_documents({"tablenumber": tablenumber}) == 0:
            order = dict()
            obj = order_collection.find_one({'$query':{},'$orderby':{'_id':-1}})
            if obj:
                max_id = obj["_id"]
            else:
                max_id = 1
            order["_id"] = max_id + 1
            order["date"] = datetime.now()
            order["items"] = [dict(itemqty) for itemqty in getItems["items"]]
            order["amount"] = int(getItems["amount"])
            order["ordernumber"] = max_id + 1
            order["tablenumber"] = tablenumber
            #return order
            _id = order_collection.insert_one(dict(order))
            current_order = order_collection.find_one({"tablenumber": tablenumber})
            return current_order
            
        else:
            added_item = [dict(itemqty) for itemqty in getItems["items"]]
            current_order = order_collection.find_one({"tablenumber": tablenumber})
            current_order["items"].extend(added_item)
            
            current_order["amount"] += getItems["amount"]
            order_collection.find_one_and_update(
                {"tablenumber": tablenumber}, 
                {"$set": current_order}
            )
            new_order = order_collection.find_one({"tablenumber": tablenumber})
            return new_order

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/changeOrder/{tablenumber}")
def change_order(tablenumber: int, getItems: GetTotalOrders):
    expired()
    getItems = dict(getItems)
    items = [dict(itemqty) for itemqty in getItems["items"]]
    current_order = order_collection.find_one({"tablenumber": tablenumber})
    current_order = dict(current_order)
    current_order["items"] = items
    current_order["amount"] = getItems["amount"]
    order_collection.find_one_and_update(
        {"tablenumber": tablenumber}, 
        {"$set": current_order}
    )
    new_order = order_collection.find_one({"tablenumber": tablenumber})
    return new_order

@router.post("/data")
def get_data(dates: Dates):
    expired()
    dates = dict(dates)
    start = dates.get("startDate", datetime.now())
    end = dates.get("endDate", datetime.now())
    all_orders = order_data_collection.find({})
    return_dict = {
        "orders": [],
        "totalOrders": 0,
        "totalAmount": 0,
        "errors": []
    }
    for each_order in all_orders:
        try:
            each_order = dict(each_order)
            if start <= each_order["date"] <= end:
                return_dict["orders"].append(each_order)
                return_dict["totalAmount"] += each_order["amount"]
        except Exception as e:
            return_dict["errors"].append(str(e))
    return_dict["totalOrders"] = len(return_dict["orders"])
    return return_dict
