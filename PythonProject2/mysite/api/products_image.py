from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import ProductImage
from mysite.database.schema import ProductImageInputSchema, ProductImageOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

products_image_router = APIRouter(prefix='/products-image', tags=['ProductImage'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@products_image_router.post('/', response_model=ProductImageOutSchema)
async def create_product_image(product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    product_image_db = ProductImage(**product_image.dict())
    db.add(product_image_db)
    db.commit()
    db.refresh(product_image_db)
    return product_image_db


@products_image_router.get('/', response_model=List[ProductImageOutSchema])
async def list_product_images(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@products_image_router.get('/{image_id}', response_model=ProductImageOutSchema)
async def detail_product_image(image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not product_image_db:
        raise HTTPException(detail="Product image not found", status_code=404)
    return product_image_db


@products_image_router.put('/{image_id}', response_model=ProductImageOutSchema)
async def update_product_image(image_id: int, product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not product_image_db:
        raise HTTPException(detail="Product image not found", status_code=404)

    for key, value in product_image.dict().items():
        setattr(product_image_db, key, value)

    db.commit()
    db.refresh(product_image_db)

    return product_image_db


@products_image_router.delete('/{image_id}')
async def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not product_image_db:
        raise HTTPException(detail="Product image not found", status_code=404)

    db.delete(product_image_db)
    db.commit()

    return {'message': 'Product image deleted'}