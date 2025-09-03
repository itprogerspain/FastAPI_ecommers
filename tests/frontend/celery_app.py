from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery.autodiscover_tasks(["tests.frontend"])

# celery.conf.task_routes = {
#     "tests.frontend.tasks.high_priority_task": {"queue": "high_priority"},
#     "tests.frontend.tasks.low_priority_task": {"queue": "low_priority"},
# }

