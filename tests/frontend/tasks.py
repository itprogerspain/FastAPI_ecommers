import time
from .celery_app import celery

@celery.task(queue="high_priority")
def high_priority_task():
    time.sleep(2)
    print("Execution of a high-priority task")

@celery.task(queue="low_priority")
def low_priority_task(message: str):
    time.sleep(2)
    print("Execution of a low-priority task:", message)
