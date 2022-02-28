from pydantic import BaseModel
from typing import List
from datetime import datetime
from itemAPI.models import Item
from fastapi import WebSocket

class OrderItem(BaseModel):
    name: str
    price: int
    veg: int
    type: str
    qty: int

class Dates(BaseModel):
    startDate: datetime
    endDate: datetime

class GetTotalOrders(BaseModel):
    amount: int
    items: List[OrderItem]
class ItemQty(Item):
    """
    This class adds quantity to item class
    """
    qty: int

class GetItems(BaseModel):
    amount: int
    items: List[ItemQty]

class Order(BaseModel):
    _id: int
    date: datetime
    items: List[ItemQty]
    amount: int
    tablenumber: str
    ordernumber: int
    paymentMethod: str

class PaymentMethod(BaseModel):
    paymentMethod: str

class Stats(BaseModel):
    month: int
    year: int

class ConnectionManager:
    def __init__(self) -> None:
        self.connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, name: str):
        await websocket.accept()
        self.connections.append((websocket, name))
        with open("webs.txt", "a") as fp:
            fp.write(f"\n{str(self.connections[1])}")
    
    def disconnect(self, websocket: WebSocket, name: str):
        self.connections.remove((websocket, name))
    
    async def broadcast(self, data: str):
        for connection, name in self.connections:
            with open("webrecv.txt", "a") as fp:
                fp.write(f"\n{str(connection), name, str(name)}")
                if str(name) in 'wne':
                    fp.write(f"\nSENT => {name, str(name)} < SENT")
                    await connection.send_text(f"{data}")
