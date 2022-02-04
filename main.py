import uvicorn
from fastapi import FastAPI
from itemAPI.routers import router as itemRouter
from ordersAPI.routers import router as orderRouter
from utils.routers import router as utilRouter


app = FastAPI()
app.include_router(itemRouter)
app.include_router(orderRouter)
app.include_router(utilRouter)


@app.get('/')
async def root():
    return {"message": "Hey from dev!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
