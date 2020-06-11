from datetime import timedelta

from bson import ObjectId
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import fields
from werkzeug.security import safe_str_cmp

from db import userRegister, Token
from utils import parse_req, send_error, check_input,send_result

account = Blueprint('account', __name__)
ACCESS_EXPIRES = timedelta(days=30)


@account.route('/register', methods=['POST'])
def register_account():
    """
    This method should add another user
    :return: A notification of successful
    """
    params = {
        'username': fields.String(),
        'password': fields.String()
    }
    json_data = parse_req(params)
    try:
        username = json_data.get('username', None)
        password = json_data.get('password', None)
    except:
        return send_error(code=500)
    query_account = {
        'username': username,
        'password': password
    }

    find_username = userRegister.find({}, {'username': 1, '_id': 0})
    for user in find_username:
        if user['username'] == username:
            return jsonify("This account is already exist !")

    try:
        result = userRegister.insert_one(query_account)
        return send_result(result)
    except:
        return send_error(code=500)


@account.route('/login', methods=['POST'])
def login():
    """
    This methods uses to login  in order to gain access token
    :return: access token
    """
    param = {
        'username': fields.String(),
        'password': fields.String()
    }
    try:
        json_data = parse_req(param)
        username = json_data.get('username', None)
        password = json_data.get('password', None)
    except :
        return jsonify("An error occurred when getting data !")

    user = userRegister.find_one({'username': username})

    if not safe_str_cmp(user['password'], password):
        return jsonify("Your password is wrong!")

    access_token = create_access_token(identity=str(user['_id']), expires_delta=ACCESS_EXPIRES)

    dict1 = {
        'access_token': access_token,
        'message': 'Login Successfully !'
    }
    user_token = dict(
        _id=str(ObjectId()),
        person_id=user['_id'],
        access_token=access_token,
    )
    Token.insert_one(user_token)

    return jsonify(dict1)
