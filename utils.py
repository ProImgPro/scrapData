from webargs.flaskparser import FlaskParser
from flask import jsonify
import re

parser = FlaskParser()


def parse_req(argmap):
    """

    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def send_result(data=None, message='OK', code=200, status=True):
    """
    :param data: The search_data to respond
    :param message: The message to respond
    :param code: The code of HTTP (2xx, 3xx, 4xx, 5xx)
    :param status: Status is true or false.
    :return: The returned response contains search_data and code.

    res = {
        'status': status,
        'code': code,
        'message': message,
        'search_data': search_data,
    }
    """
    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code


def send_error(message='Failed', code=200, status=False,data=None):
    """
    :param data: The search_data to respond
    :param message: The message to respond
    :param code: The code of HTTP (2xx, 3xx, 4xx, 5xx)
    :param status: Status is true or false.
    :return: The returned response contains search_data and code.
    res = {
        'jsonrpc': '2.0',
        'status': status,
        'code': code,
        'message': message,
        'search_data': search_data,
    }
    """
    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code

def check_input(data):
    """

    :param data:
    :return:
    """
    if not re.match("^[A-Za-z1-9]*$", data):
        return None
    return 'Ok'
