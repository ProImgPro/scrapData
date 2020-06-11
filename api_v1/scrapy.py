import requests
from bs4 import BeautifulSoup
from flask import Blueprint
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from db import news, href
from utils import send_result,send_error
from flask import jsonify

crawl = Blueprint('crawl', __name__)


def retry_session(retries, session=None, backoff_factor=0.3):
    """
    Use to handle internet interupt
    :param retries: 10
    :param session:
    :param backoff_factor: 0.3
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        method_whitelist=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('https://', adapter)
    return session


@crawl.route('/links', methods=['GET'])
def get_all_link():
    """
    Insert link into db
    and update new link whenever source code changed
    :return:
    """
    i = 2
    while True:
        if len(retry_session(10).get(f'https://vnexpress.net/giao-duc-p{i}').history) == 0:
            url = retry_session(10).get(f'https://vnexpress.net/giao-duc-p{i}').text
            soup = BeautifulSoup(url, 'html.parser')
            link_web = soup.select('.meta-news>.count_cmt')
            for link_website in link_web:
                if href.find_one( {'link': link_website['href']}) is None:
                    href.insert({'link': link_website['href']})
            i = i + 1
        else:
            break

def crawl_data(url):
    """
    This function will crawl content and title of all page
    program will stop when losing network and immediately crawl again whenever connecting network
    :param
    :return: a notification of success
    """
    link = retry_session(10).get(url).text
    soup = BeautifulSoup(link, 'html.parser')
    try:
        if news.find_one({'link': url}) is None:
            content = soup.select('.fck_detail>p')
            content_text = str.join('\n', [p.get_text() for p in content])
            title = soup.select_one('.title-detail').get_text()
            data = {
                'content': content_text,
                'title': title,
                'link': url
            }
            news.insert(data)
    except Exception as e:
            print({e})


