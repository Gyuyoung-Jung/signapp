# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, jsonify, abort
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime, timedelta
import json
import requests

from app import app, db
from app.user.models import User


# CONFIG
user_blueprint = Blueprint('user', __name__, url_prefix='/user')


def getUserProfile(access_token):
    header = "Bearer " + access_token
    url = "https://openapi.naver.com/v1/nid/me"
    req = urllib.request.Request(url)
    req.add_header("Authorization", header)
    response = urllib.request.urlopen(req)
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read().decode('utf8')
        return response_body
    else:
        return None


@user_blueprint.route('/', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        ret_json = {}
        code = str(request.args.get('code'))
        state = str(request.args.get('state'))

        if state != 'test':
            success = "false"
            message = "state 값 실패"
            data = None
            ret_json = {
                "success": success,
                "message": message,
                "data": data
            }
            return jsonify(ret_json)

        url = "https://nid.naver.com/oauth2.0/tokenA"
        payload = "grant_type=authorization_code&client_id=AlqPsEE8Jcobo0KCNHVC&client_secret=iabjXGYD01&code=" \
                  + str(code) + "&state="+state
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        access_token = json.loads(((response.text).encode('utf-8')))['access_token']

        response_body = getUserProfile(access_token)

        if response_body is not None:
            user_profile = json.loads(response_body)
            print(user_profile)
            print(user_profile['response'])
            user_profile = user_profile['response']
            nid = user_profile['id']
            email = user_profile['email']
            name = user_profile['name']

            user = User.query.filter_by(nid=nid, email=email).first()

            if user is None:
                success = "false"
                message = "register please"
                data = None
                ret_json = {
                    "success": success,
                    "message": message,
                    "data": data
                }
                return jsonify(ret_json)
            else:
                success = "true"
                message = "register success"
                data = {
                    "name": name,
                    "email": email
                }
                ret_json = {
                    "success": success,
                    "message": message,
                    "data": data
                }
                return jsonify(ret_json)
        else:
            success = "false"
            message = "response is not valid"
            data = None
            ret_json = {
                "success": success,
                "message": message,
                "data": data
            }
            return jsonify(ret_json)

    elif request.method == "GET":
        success = "True"
        message = "not yet"
        data = None
        ret_json = {
            "success": success,
            "message": message,
            "data": data
        }
        return jsonify(ret_json)


@user_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def user_detail(id):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()

        if user is not None:
            ret_json = {
                "success": "true",
                "message": "user profile",
                "data": {
                    "id": user.id,
                    "nid": user.nid,
                    "email": user.email
                }
            }
            return jsonify(ret_json)
        else:
            ret_json = {
                "success": "false",
                "message": "user not exist",
                "data": None
            }
            return jsonify(ret_json)
