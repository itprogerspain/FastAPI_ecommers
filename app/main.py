from fastapi import FastAPI
from app.routers import category, products, auth
from app.config import settings
from app.routers import permission, reviews

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(reviews.router)


@app.get("/key")
def get_key():
    return {"secret_key": settings.SECRET_KEY}