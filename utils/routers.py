from fastapi import APIRouter
from mongosetup.mongodb import expire_collection

router = APIRouter(
    prefix="/servercontrol",
    tags=["utils"],
    responses={404: {"description": "order not available!"}},
)

@router.get('/server/stop')
def root():
    op = expire_collection.find_one({"_id":1})
    op['services'] = 0
    expire_collection.find_one_and_update({"_id": 1}, {"$set": op})
    return {"status": 200}

@router.get('/server/start')
def root():
    op = expire_collection.find_one({"_id":1})
    op['services'] = 1
    expire_collection.find_one_and_update({"_id": 1}, {"$set": op})
    return {"status": 200}