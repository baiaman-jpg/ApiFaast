from passlib.context import CryptContext

from fastapi import APIRouter, HTTPException, Depends
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema,UserProfileLoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



@auth_router.post("/register", response_model=dict)
async def register (user: UserProfileInputSchema, db: Session = Depends(get_db)):
    hash_password=get_password_hash(user.password)
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if email_db:
        raise HTTPException(detail="Email already registered", status_code=400)

    new_db=UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=hash_password,
        age = user.age,
        avatar=user.avatar,
        status=user.status,
        number=user.phone_number,
    )

    db.add(new_db)
    db.commit()
    db.refresh(new_db)
    return {'message': 'success',}




@auth_router.post("/login", response_model=dict)
async def login(user: UserProfileLoginSchema, db: Session = Depends(get_db)):
    username_db=db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db=db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if not username_db or not email_db or not verify_password(user.password, username_db.password):
        raise HTTPException(
            detail="Username not found",
            status_code=400,
        )
    return {'message': 'success',}

