from fastapi import FastAPI
import uvicorn

from mysite.api.category import category_router
from mysite.api.users import users_router
from mysite.api.products_image import products_image_router
from mysite.api.products import product_router
from mysite.api.rating import rating_router
from mysite.api.subcategory import subcategory_router
from mysite.api.auth import auth_router




store_app = FastAPI()
store_app.include_router(users_router)
store_app.include_router(category_router)
store_app.include_router(products_image_router)
store_app.include_router(product_router)
store_app.include_router(rating_router)
store_app.include_router(subcategory_router)
store_app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(store_app, host="127.0.0.1", port=8000)