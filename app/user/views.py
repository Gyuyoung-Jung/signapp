# IMPORTS
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required, logout_user
import json
import urllib
import MySQLdb

from app import app, db
from app.user.models import User


# CONFIG
user_blueprint = Blueprint('user', __name__, url_prefix='/user')


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


@user_blueprint.route('', methods=['GET', 'POST'])
def users():
    if request.method == "POST":
        try:
            access_token = request.json.get('access_token')
            # access_token = request.form['access_token']
            nickname = request.json.get('nickname')
            sns = request.json.get('sns')
            push_token = request.json.get('push_token')
            get_push = request.json.get('get_push')
            device = request.json.get('device')

            if access_token is None:
                ret_json = {
                    "success": "false",
                    "message": "Access Token is Null",
                }
                return jsonify(ret_json), 400

            response_body = getUserProfile(access_token, sns)

            if response_body is not None:
                if sns == 'N':
                    user_profile = parseNaverResponseBody(response_body)
                    user_profile = user_profile['response']
                    nid = user_profile['id']
                    kid = None
                    email = user_profile['email']
                    nickname = user_profile['nickname']
                elif sns == 'K':
                    user_profile = parseKakaoResponseBody(response_body)
                    nid = None
                    kid = user_profile['id']
                    email = user_profile['kakao_account']['email']
                    nickname = user_profile['kakao_account']['profile']['nickname']
                # user_profile = json.loads(response_body)

            new_user = User(nid, kid, email, None, nickname, get_push, device)
            db.session.add(new_user)
            db.session.commit()

            ret_json = {
                "success": "true",
                "message": "user register success",
                "data": {
                    "email": email,
                    "nickname": nickname
                }
            }
            return jsonify(ret_json)

        except MySQLdb.IntegrityError as ie:
            print(ie)
            ret_json = {
                "success": "false",
                "message": "User Exist"
            }
            return jsonify(ret_json), 409

        except Exception as e:
            print(e)
            ret_json = {
                "success": "false",
                "message": "user register failed",
            }
            return jsonify(ret_json), 400


@user_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def user(id):
    if current_user.id != id:
        ret_json = {
            "success": "false",
            "message": "User Id Incorrect",
            "data": None
        }
        return jsonify(ret_json)

    if request.method == "GET":
        try:
            user_profile = User.query.filter_by(id=id).first()
        except Exception as e:
            print("db error")
            ret_json = {
                "success": "false",
                "message": "db error",
                "data": None
            }
            return jsonify(ret_json)

        if user_profile is None:
            ret_json = {
                "success": "false",
                "message": "Not Registered User",
                "data": None
            }
            return jsonify(ret_json)
        else:
            ret_json = {
                "success": "true",
                "message": "register success",
                "data": {
                    "name": user_profile.name,
                    "email": user_profile.email,
                    "nickname": user_profile.nicknam
                }
            }
            return jsonify(ret_json)

    elif request.method == "PUT":
        try:
            access_token = request.json.get('access_token')
            nickname = request.json.get('nickname')
            sns = request.json.get('sns')
            push_token = request.json.get('push_token')
            get_push = request.json.get('get_push')
            device = request.json.get('device')
            user = User.query.filter_by(id=id).first()

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
                    kid = None
                    email = user_profile['email']
                    nickname = user_profile['nickname']
                elif sns == 'K':
                    user_profile = parseKakaoResponseBody(response_body)
                    nid = None
                    kid = user_profile['id']
                    email = user_profile['kakao_account']['email']
                    nickname = user_profile['kakao_account']['profile']['nickname']

            if (sns == 'N' and user.nid != nid) or (sns == 'K' and user.kid != kid):
                ret_json = {
                    "success": "false",
                    "message": "naver profile not eq db profile",
                    "data": {
                        "email": email
                    }
                }
                return jsonify(ret_json)
            else:
                user.nickname = nickname
                user.push_token = push_token
                user.get_push = get_push
                user.device = device
                db.session.commit()

                ret_json = {
                    "success": "true",
                    "message": "update success",
                    "data": {
                        "id": id,
                        "email": user.email,
                        "nickname": nickname
                    }
                }
                return jsonify(ret_json)

        except Exception as e:
            ret_json = {
                "success": "false",
                "message": "update failed",
                "data": {
                    "id": id,
                    "email": user.email,
                    "nickname": user.nickname
                }
            }
            print(e)
            return jsonify(ret_json)
    elif request.method == "DELETE":
        try:
            access_token = request.form['access_token']
            if access_token is None:
                ret_json = {
                    "success": "false",
                    "message": "Access Token is Null",
                    "data": None
                }
                return jsonify(ret_json)

            response_body = getUserProfile(access_token)

            if response_body is not None:
                user_profile = json.loads(response_body)
                user_profile = user_profile['response']
                nid = user_profile['id']
                email = user_profile['email']

            user = User.query.filter_by(id=id).first()
            if user.nid != nid:
                ret_json = {
                    "success": "false",
                    "message": "naver profile not eq db profile",
                }
                return jsonify(ret_json)
            else:
                db.session.delete(user)
                db.session.commit()

                ret_json = {
                    "success": "true",
                    "message": "delete user success",
                    "data": {
                        "email": email
                    }
                }
                logout_user()
                return jsonify(ret_json)
        except Exception as e:
            print(e)
