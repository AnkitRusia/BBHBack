from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
from ordersAPI.models import  GetItems, Stats, ConnectionManager
from mongosetup.mongodb import order_collection, order_data_collection
from datetime import datetime
from utils.common import expired

  
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

@router.get("/{tablenumber}")
def get_order(tablenumber: str):
    expired()
    try:
        current_order = order_collection.find_one({"tablenumber": tablenumber})
        return current_order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/paid/{tablenumber}")
def delete_bill_paid(tablenumber: str):
    expired()
    try:
        order = order_collection.find_one({"tablenumber": tablenumber})
        max_id = order_data_collection.find_one({'$query':{},'$orderby':{'_id':-1}})["_id"]
        order["_id"] = max_id + 1
        order_data_collection.insert_one(order)
        order_collection.find_one_and_delete({"tablenumber": tablenumber})
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/del/{tablenumber}")
def delete_clear_table_lost_customer(tablenumber: str):
    try:
        order_collection.find_one_and_delete({"tablenumber": tablenumber})
        return {"status": 200}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{tablenumber}")
def new_order(tablenumber: str, getItems: GetItems):
    expired()
    getItems = dict(getItems)
    try:
        if order_collection.count_documents({"tablenumber": tablenumber}) == 0:
            order = dict()
            max_id = order_collection.find_one({'$query':{},'$orderby':{'_id':-1}})["_id"]
            order["_id"] = max_id + 1
            order["date"] = datetime.now()
            order["items"] = [dict(itemqty) for itemqty in getItems["items"]]
            order["amount"] = int(getItems["amount"])
            order["ordernumber"] = max_id
            order["tablenumber"] = tablenumber
            #return order
            _id = order_collection.insert_one(dict(order))
            return _id
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

@router.put("/{tablenumber}")
def change_order(tablenumber: str, getItems: GetItems):
    expired()
    getItems = dict(getItems)
    items = [dict(itemqty) for itemqty in getItems["items"]]
    current_order = order_collection.find_one({"tablenumber": tablenumber})
    current_order["items"] = items
    current_order["amount"] = getItems["amount"]
    order_collection.find_one_and_update(
        {"tablenumber": tablenumber}, 
        {"$set": current_order}
    )
    new_order = order_collection.find_one({"tablenumber": tablenumber})
    return new_order


