# IMPORTS
from flask import Blueprint, request, url_for, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from app import app, db
from app.user.models import User

import requests
import urllib
import json


# CONFIG
auth_blueprint = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')


def getUserProfile(access_token, sns):
    header = "Bearer " + access_token
    if sns == "N":
        url = "https://openapi.naver.com/v1/nid/me"
    elif sns == "K":
        url = "https://kapi.kakao.com/v2/user/me"

    req = urllib.request.Request(url)
    req.add_header("Authorization", header)
    response = urllib.request.urlopen(req)
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read().decode('utf8')
        return response_body
    else:
        return None


def parseNaverResponseBody(response_body):
    data = response_body.json()

    return data


def parseKakaoResponseBody(response_body):
    data = json.loads(response_body)

    return data


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            access_token = request.args.get('access_token')
            sns = request.args.get('sns')
        except Exception as e:
            ret_json = {
                "success": "false",
                "message": "None Access Token",
                "data": None
            }
            return jsonify(ret_json)
        try:
            if access_token is None:
                ret_json = {
                    "success": "false",
                    "message": "Access Token is Null",
                    "data": None
                }
                return jsonify(ret_json)

            response_body = getUserProfile(access_token, sns)

            if response_body is not None:
                if sns == 'N':
                    user_profile = parseNaverResponseBody(response_body)
                    user_profile = user_profile['response']
                    nid = user_profile['id']
                    email = user_profile['email']
                    user = User.query.filter_by(nid=nid, email=email).first()
                elif sns == 'K':
                    user_profile = parseKakaoResponseBody(response_body)
                    kid = user_profile['id']
                    email = user_profile['kakao_account']['email']
                    user = User.query.filter_by(kid=kid, email=email).first()

                if user is not None:
                    user.authenticated = True
                    user.last_logged_in = user.current_logged_in
                    user.current_logged_in = datetime.now()
                    user.access_token = access_token
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)

                    ret_json = {
                        "success": "true",
                        "message": "login succeed",
                        "data": {
                            "id": user.id,
                            "email": email,
                            "nickname": user.nickname
                        }
                    }

                    return jsonify(ret_json)

                else:
                    ret_json = {
                        "success": "false",
                        "message": "login failed. not user",
                        "data": None
                    }
                    return jsonify(ret_json)
            else:
                ret_json = {
                    "success": "false",
                    "message": "sns login failed",
                    "data": None
                }
                return jsonify(ret_json)
        except Exception as e:
            print(e)
            ret_json = {
                "success": "false",
                "message": "Get SNS User Failed",
                "data": None
            }
            return jsonify(ret_json)
    elif request.method == "POST":
        ret_json = {
            "success": "false",
            "message": "POST"
        }
        return jsonify(ret_json)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        user = current_user
        user.authenticated = False

        db.session.add(user)
        db.session.commit()

        ret_json = {
            "success": "true",
            'message': 'success',
            'data': {
                'nid': user.nid,
                'email': user.email,
            }
        }

        logout_user()
        user = current_user
        return jsonify(ret_json)
    except Exception as e:
        ret_json = {
            "success": "false",
            "message": "Logout Failed",
            "data": {
                "nid": user.nid,
                "email": user.email
            }
        }
        return jsonify(ret_json)


