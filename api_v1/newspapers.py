from bson import ObjectId
from flask import Blueprint, jsonify, request
from marshmallow import fields

from db import news
from utils import send_result, send_error, check_input,parse_req

post = Blueprint('post', __name__)


@post.route('/title', methods=['GET'])
def get_all_data():
    """
    This method should get all contents and titles in db
    :return: content and title in db
    """
    all_data = news.find({}, {'_id': 0})
    results = []
    for data in all_data:
        results.append(data)

    return send_result(results)


@post.route('/news', methods=['GET'])
def get_title():
    """
    This method should find a post by its content
    :return: a post
    """
    param_title = request.args.get('title', None)
    query_title = {
        'title': param_title
    }
    if check_input(param_title):
        find_title = news.find_one(query_title)
        if find_title:
            page_size = request.args.get('page_size', '0')
            page_number = request.args.get('page_number', '0')
            skips = int(page_size) * int(page_number)
            find_data = list(news.find(query_title, {'_id': 0}).skip(skips).limit(int(page_size)))
            return send_result(find_data)
        return send_error(code=404, message="Title doesn't exist")
    return  send_error(code=406, message="Invalid title")

@post.route('/news', methods=['POST'])
# @jwt_required
def add_post():
    """
    This method should add a new post in db
    :return: a notification of successful or errors
    """
    params = {
        'title': fields.String(),
        'content': fields.String()
    }
    json_data = parse_req(params)
    content = json_data.get("content", None)
    if check_input(content):
        return send_error(code=406, message="Content contains special characters")
    title = json_data.get('title', None)
    if check_input(title):
        return send_error(code=406, message="Title contains special characters")
    query_data = {
        '_id': str(ObjectId()),
        'title': title,
        'content': content
    }
    try:
        result = news.insert(query_data)
        return send_result(result)
    except:
        return send_error(code=400)

@post.route('/news', methods=['PUT'])
# @jwt_required
def update_data_by_id():
    """
    This method should update a post by its id in db
    :return: a notification of successful or error
    """
    param_id = request.args.get('_id', None)
    query_id = {
        '_id': param_id
    }
    find_id = news.find(query_id)
    if find_id is None:
        return jsonify("_id doesn't exist!")
    params = {
        'title': fields.String(),
        'content': fields.String()
    }
    json_data = parse_req(params)
    try:
        title = json_data.get('title', None)
        content = json_data.get('content', None)
    except:
        return jsonify("Error occur when getting data !")
    new_param = {
        '$set': {
                'title': title,
                'content': content
        }
    }
    try:
        result = news.update_one(query_id, new_param)
        return send_result(result)
    except:
        return send_error(code=500)


@post.route('/news', methods=['DELETE'])
# @jwt_required
def delete_post_by_id():
    """
    This method should delete a post by its id in db
    :return: a notification of successful or error
    """
    param_id = request.args.get('_id', None)
    query_id = {
        '_id': param_id
    }
    find_id = news.find(query_id)
    if find_id is None:
        return jsonify("_id doesn't exist!")
    try:
        result = news.delete_one(query_id)
        return send_result(result)
    except:
        return send_error(code=500)

