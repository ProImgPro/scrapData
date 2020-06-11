# -*- coding: utf-8 -*-
import requests

from celery_app.workers import celery
from api_v1.scrapy import crawl_data
from db import href


import logging

_logger = logging.getLogger('app_logs.log')


@celery.task(name="task.crawl_data")
def task_crawl_data(url):
    crawl_data(url=url)

# @celery.task(name="task.crawl_data")
# def task_crawl_data():
#     urls = href.find({}, {'link': 1, '_id': 0})
#     for url in urls:
#         link = requests.get(str(url['link'])).text
#         crawl_data(link)

# links = href.find({}, {'link': 1, '_id': 0})
# for link in links:
#     print(str(link['link']))

