from fastapi import FastAPI

from app.config.database import engine, Base
from .routers.router import set_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
set_router(app)


@app.get(path="/")
def root():
    return {"message": "Hello World!"}
