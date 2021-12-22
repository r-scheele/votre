from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base
from app.routers.router import set_router

# commented it, since i'm now using Alembic for migration
# Base.metadata.create_all(bind=engine)

app = FastAPI()
set_router(app)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(path="/")
def root():
    return {"message": "send request to votres/herokuapp.com/docs to get access to the swaggerUI documentation😁 "
                       "cheers!"}
