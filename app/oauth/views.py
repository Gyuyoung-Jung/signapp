# IMPORTS
from flask import Blueprint, request, redirect, url_for, jsonify
from app.user.models import User
import urllib.request
import requests
import json
# import logging

KAKAO_CLIENT_ID = "112eb1b619716055b81170ca51fe62d9"
KAKAO_SECRET_KEY = "NTxKzHqBIyqnhXs9RRBFJP19fgyC7ckr"

# CONFIG
oauth_blueprint = Blueprint('oauth', __name__, template_folder='templates', url_prefix='/oauth')


def getUserProfile(access_token):
    try:
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
    except Exception as e:
        print(e)


@oauth_blueprint.route('/check', methods=['GET', 'POST'])
def check():
    code = str(request.args.get('code'))
    state = str(request.args.get('state'))

    if state != 'test':
        ret_json = {
            "success": "false",
            "message": "Api State Code Error",
            "data": None
        }
        return jsonify(ret_json)

    try:
        url = "https://nid.naver.com/oauth2.0/token"
        payload = "grant_type=authorization_code&client_id=AlqPsEE8Jcobo0KCNHVC&client_secret=iabjXGYD01&code=" \
                  + str(code) + "&state=test"
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
                ret_json = {
                    "success": "true",
                    "message": "New Client",
                    "data": {
                        "access_token": access_token
                    }
                }

            else:
                ret_json = {
                    "success": "true",
                    "message": "Welcome User",
                    "data": {
                        "access_token": access_token
                    }
                }

            return jsonify(ret_json)
        else:
            ret_json = {
                "success": "false",
                "message": "Please Check Your SNS Auth",
            }
            return jsonify(ret_json)
    except Exception as e:
        print(e)
        ret_json = {
            "success": "false",
            "message": "Exception Catch",
        }
        return jsonify(ret_json)


@oauth_blueprint.route('/kakao_check', methods=['GET', 'POST'])
def kakao_check():
    code = str(request.args.get('code'))
    state = str(request.args.get('state'))

    if state != 'test':
        ret_json = {
            "success": "false",
            "message": "Api State Code Error",
            "data": None
        }
        return jsonify(ret_json)

    try:
        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code&client_id="+KAKAO_CLIENT_ID+"&client_secret="+KAKAO_SECRET_KEY+"&code=" \
                  + str(code) + "&state=test"
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
                ret_json = {
                    "success": "true",
                    "message": "New Client",
                    "data": {
                        "access_token": access_token
                    }
                }

            else:
                ret_json = {
                    "success": "true",
                    "message": "Welcome User",
                    "data": {
                        "access_token": access_token
                    }
                }

            return jsonify(ret_json)
        else:
            ret_json = {
                "success": "false",
                "message": "Please Check Your SNS Auth",
            }
            return jsonify(ret_json)
    except Exception as e:
        print(e)
        ret_json = {
            "success": "false",
            "message": "Exception Catch",
        }
        return jsonify(ret_json)
