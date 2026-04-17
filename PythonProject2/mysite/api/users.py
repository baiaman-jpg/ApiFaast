from fastapi import APIRouter, HTTPException, Depends
from mysite.database.db import  SessionLocal
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema
from sqlalchemy.orm import Session
from typing import List

users_router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post('/', response_model=UserProfileInputSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db =UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@users_router.get('/', response_model =List[ UserProfileInputSchema])
async def list_users(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@users_router.get('/{id}', response_model=UserProfileInputSchema)
async def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(UserProfile).get(id)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    return user_db