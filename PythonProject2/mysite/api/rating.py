from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Rating
from mysite.database.schema import RatingSchema
from mysite.database.db import SessionLocal

rating_router = APIRouter(prefix="/rating", tags=["Rating"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@rating_router.post("/", response_model=RatingSchema)
async def create_rating(data: RatingSchema, db: Session = Depends(get_db)):
    obj = Rating(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@rating_router.get("/", response_model=List[RatingSchema])
async def list_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@rating_router.get("/{id}", response_model=RatingSchema)
async def detail_rating(id: int, db: Session = Depends(get_db)):
    obj = db.query(Rating).filter(Rating.id == id).first()
    if not obj:
        raise HTTPException(404, "Rating not found")
    return obj


@rating_router.put("/{id}", response_model=RatingSchema)
async def update_rating(id: int, data: RatingSchema, db: Session = Depends(get_db)):
    obj = db.query(Rating).filter(Rating.id == id).first()
    if not obj:
        raise HTTPException(404, "Rating not found")

    for key, value in data.dict().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@rating_router.delete("/{id}")
async def delete_rating(id: int, db: Session = Depends(get_db)):
    obj = db.query(Rating).filter(Rating.id == id).first()
    if not obj:
        raise HTTPException(404, "Rating not found")

    db.delete(obj)
    db.commit()
    return {"message": "Rating deleted"}