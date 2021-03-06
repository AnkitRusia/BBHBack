from pydantic import BaseModel
from typing import List
from datetime import datetime
from itemAPI.models import Item
from fastapi import WebSocket


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

class Stats(BaseModel):
    month: int
    year: int

class ConnectionManager:
    def __init__(self) -> None:
        self.connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, name: str):
        await websocket.accept()
        self.connections.append((websocket, name))
    
    def disconnect(self, websocket: WebSocket, name: str):
        self.connections.remove((websocket, name))
    
    async def broadcast(self, to_name: str):
        for connection, name in self.connections:
            if name == 'owner':
                await connection.send_text(f"notification received")
