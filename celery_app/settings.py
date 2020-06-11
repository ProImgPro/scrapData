from celery.schedules import crontab

CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

REDIS_URL = 'redis://localhost:6379'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


CELERYBEAT_SCHEDULE = {
    'celery-tasks': {
        'task': 'task.test',
        'schedule': crontab(minute='*'),

    }

}



