from fastapi import FastAPI
from db.router import router

app = FastAPI()
app.include_router(router)
