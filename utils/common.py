from mongosetup.mongodb import expire_collection
from datetime import datetime
from fastapi import HTTPException, status

def expired():
    op = expire_collection.find_one({"_id":1})
    expire_date = op['endDate']
    service = op['services']
    now = datetime.now()
    if expire_date < now:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Please renew your softare")
    if service != 1:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Services will be off")
        
    