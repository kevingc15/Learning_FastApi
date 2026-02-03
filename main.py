from routers import users, products
# from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
# app.mount("/static", StaticFiles(directory="static"), name="static")