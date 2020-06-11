from celery import Celery
import celery_app.settings as config_celery


celery = Celery('celery_app.workers', broker=config_celery.CELERY_BROKER_URL)
