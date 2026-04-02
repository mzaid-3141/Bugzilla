from fastapi import FastAPI
from router import router

import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@router.get("/")
def root():
    return {"message": "Router working"}