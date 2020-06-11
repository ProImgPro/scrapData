from flask import Flask
from api_v1.scrapy import crawl_data
from api_v1.newspapers import post
from api_v1.accounts import account
from api_v1.scrapy import crawl

app = Flask(__name__)

app.register_blueprint(newspapers.post, url_prefix='/post')
app.register_blueprint(accounts.account, url_prefix='/account')
app.register_blueprint(scrapy.crawl, url_prefix='/crawl')

