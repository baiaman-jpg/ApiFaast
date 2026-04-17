from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional, List


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    age: Optional[int]
    phone_number: Optional[str]
    avatar: Optional[str]
    status: str
    created_date: date


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    age: Optional[int]
    phone_number: Optional[str]
    avatar: Optional[str]
    status: str
    created_date: date

    class Config:
        from_attributes = True


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str
    email: str



class CategoryInputSchema(BaseModel):
    category_name: str
    category_image_url: str


class CategoryOutSchema(BaseModel):
    id: int
    category_name: str
    category_image_url: str

    class Config:
        from_attributes = True



class SubCategoryInputSchema(BaseModel):
    sub_category_name: str
    category_id: int


class SubCategoryOutSchema(BaseModel):
    id: int
    sub_category_name: str
    category_id: int

    class Config:
        from_attributes = True


class ProductImageInputSchema(BaseModel):
    product_id: int
    image: str


class ProductImageOutSchema(BaseModel):
    id: int
    product_id: int
    image: str

    class Config:
        from_attributes = True


class ProductInputSchema(BaseModel):
    product_name: str
    price: int
    article: int
    description: str
    subcategory_id: int
    product_video: Optional[str] = None


class ProductOutSchema(BaseModel):
    id: int
    product_name: str
    price: int
    article: int
    description: str
    subcategory_id: int
    product_video: Optional[str]
    created_date: date

    product_images: List[ProductImageOutSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class RatingSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    stars: int
    text: str
    created_date: datetime

    class Config:
        from_attributes = True