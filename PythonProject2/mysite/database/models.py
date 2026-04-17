from typing import Optional, List
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, SmallInteger, DateTime
from enum import Enum as PyEnum
from datetime import date, datetime


class STATUS_CHOICES(str, PyEnum):
    gold = "Gold"
    silver = "Silver"
    bronze = "Bronze"


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String(32))
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[STATUS_CHOICES] = mapped_column(Enum(STATUS_CHOICES), nullable=False, default=STATUS_CHOICES.bronze)
    created_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    rating_user: Mapped[List['Rating']] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String, nullable=True)
    category_image_url: Mapped[str] = mapped_column(String, nullable=True)

    subcategory_name: Mapped[List['SubCategory']] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )


class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_category_name: Mapped[str] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)

    category: Mapped['Category'] = relationship(
        back_populates="subcategory_name"
    )

    # 🔥 FIX: было mapped_column → стало relationship
    product_sub: Mapped[List['Product']] = relationship(
        back_populates="subcategory",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String, default=64)
    price: Mapped[int] = mapped_column(Integer)
    article: Mapped[int] = mapped_column(Integer, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('sub_category.id'), nullable=True)

    subcategory: Mapped['SubCategory'] = relationship(
        back_populates="product_sub"
    )

    product_video: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    product_images: Mapped[List['ProductImage']] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )

    product_ratings: Mapped[List['Rating']] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )


class ProductImage(Base):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)

    product: Mapped['Product'] = relationship(
        back_populates="product_images"
    )

    product_image_url: Mapped[str] = mapped_column(String, nullable=True)


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), nullable=True)

    user: Mapped['UserProfile'] = relationship(
        back_populates="rating_user"
    )

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)

    # 🔥 FIX: было products → стало product
    product: Mapped['Product'] = relationship(
        back_populates="product_ratings"
    )

    stars: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    careated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)