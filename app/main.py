from fastapi import FastAPI

from app.config.database import engine, Base
from app.routers.router import set_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
set_router(app)


@app.get(path="/")
def root():
    return {"message": "send a  request to /docs to get access to the swaggerUI documentation😁 cheers!"}
