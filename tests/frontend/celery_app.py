from celery import Celery
from celery.schedules import crontab


celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery.autodiscover_tasks(["tests.frontend"])


celery.conf.beat_schedule = {
    'call-background-task-every-60-seconds': {
        'task': 'tests.frontend.tasks.call_background_task',
        'schedule': 60.0,  # каждые 60 секунд
        'args': ()        # аргументы нет
    }
}


# Пример Crontab (по времени, например каждый день в 7:00)
# celery.conf.beat_schedule['daily-task'] = {
#     'task': 'tests.frontend.tasks.call_background_task',
#     'schedule': crontab(hour=7, minute=0),
#     'args': ()
# }



# celery.conf.task_routes = {
#     "tests.frontend.tasks.high_priority_task": {"queue": "high_priority"},
#     "tests.frontend.tasks.low_priority_task": {"queue": "low_priority"},
# }

