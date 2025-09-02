import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from rq import Queue
from tests.frontend.tasks import call_background_task


app = FastAPI()


# Читаем адрес Redis из переменных окружения (compose их подставит)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
# redis_conn = Redis(host="localhost", port=6379, db=0)
task_queue = Queue(connection=redis_conn)

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





@app.get("/")
async def root():
    return {"message": "My test app is up"}





@app.get("/run-task/")
async def run_task(name: str):
    # Добавляем задачу в очередь Redis
    job = task_queue.enqueue(call_background_task, name)
    return {"message": f"Task {job.id} added to queue"}