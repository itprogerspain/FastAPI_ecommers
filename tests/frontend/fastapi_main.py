from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tests.frontend.tasks import high_priority_task, low_priority_task


app = FastAPI()


origins = [
    "http://localhost:3000",  # адрес локального сервера для HTML
    "null",                   # разрешаем локальные файлы через file://
]

# команда запуска данного приложения до использования докера
# uvicorn tests.frontend.fastapi_main:app --reload --port 3000

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/run-high")
async def run_high():
    high_priority_task.delay()
    return {"status": "High priority task sent"}


@app.get("/run-low")
async def run_low(message: str = "Hello from Celery"):
    low_priority_task.apply_async(args=[message], countdown=60*5)
    return {"status": f"Low priority task sent with message: {message}"}