from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routers import category, products, auth, permission, reviews, session
from app.config import settings


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(reviews.router)
app.include_router(session.router)



# ВНИМАНИЕ: этот эндпоинт используется только для учебных целей (отладка).
# В реальном приложении секретный ключ нельзя выдавать наружу!
# @app.get("/key")
# def get_key():              # для отладки
#     return {"secret_key": settings.SECRET_KEY}