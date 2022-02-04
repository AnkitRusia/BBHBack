from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    category: str
    price: List[int]
    veg: int

class Category(BaseModel):
    _id: int
    number: int
    category: List[str]
