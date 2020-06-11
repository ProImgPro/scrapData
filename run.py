import requests
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from api_v1 import app
from celery_app.workers import celery
from db import href


app.config['JSON_AS_ASCII'] = True
app.config['SECRET_KEY'] = 'SOHARDa@'

jwt = JWTManager(app)


def crawl_data_by_celery():
    """
    Use celery to crawl data from website in order to increase speed
    :return:
    """
    for link in href.find({}, {'link': 1, '_id': 0}):
        url = str(link['link'])
        celery.send_task('task.crawl_data', (url,))


with app.app_context():
    crawl_data_by_celery()


if __name__ == '__main__':
    app.run(debug=True)
