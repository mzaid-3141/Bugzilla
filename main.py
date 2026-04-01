from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from router import router

import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(router)