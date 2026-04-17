from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import SubCategory
from mysite.database.schema import SubCategoryInputSchema, SubCategoryOutSchema
from mysite.database.db import SessionLocal

subcategory_router = APIRouter(prefix="/subcategory", tags=["SubCategory"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CREATE
@subcategory_router.post("/", response_model=SubCategoryOutSchema)
async def create_subcategory(data: SubCategoryInputSchema, db: Session = Depends(get_db)):
    obj = SubCategory(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@subcategory_router.get("/", response_model=List[SubCategoryOutSchema])
async def list_subcategories(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()


@subcategory_router.get("/{id}", response_model=SubCategoryOutSchema)
async def detail_subcategory(id: int, db: Session = Depends(get_db)):
    obj = db.query(SubCategory).filter(SubCategory.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return obj


@subcategory_router.put("/{id}", response_model=SubCategoryOutSchema)
async def update_subcategory(id: int, data: SubCategoryInputSchema, db: Session = Depends(get_db)):
    obj = db.query(SubCategory).filter(SubCategory.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="SubCategory not found")

    obj.sub_category_name = data.sub_category_name
    obj.category_id = data.category_id

    db.commit()
    db.refresh(obj)
    return obj


@subcategory_router.delete("/{id}")
async def delete_subcategory(id: int, db: Session = Depends(get_db)):
    obj = db.query(SubCategory).filter(SubCategory.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="SubCategory not found")

    db.delete(obj)
    db.commit()
    return {"message": "SubCategory deleted"}