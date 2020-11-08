# IMPORTS
from flask import render_template, Blueprint, request, redirect, \
    url_for, flash, Markup, abort, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime, timedelta

from app import app, db
from app.approval.models import Approval

import requests
import json


# CONFIG
approval_blueprint = Blueprint('approval', __name__, template_folder='templates', url_prefix='/approval')


@approval_blueprint.route('/user/<int:id>', methods=['GET'])
@login_required
def list_by_user_id(id):
    try:
        type = request.args.get('type')
        state = request.args.get('state')
        page = request.args.get('page')
        count = request.args.get('count')

        user = current_user

        if user.id != id:
            ret_json = {
                "success": "false",
                "message": "로그인 user id와 일치하지 않습니다",
                "data": {
                    "user_id": id
                }
            }
            return jsonify(ret_json)

        if type == "R":
            approval_list = Approval.query.filter_by(receiver_id=user.id).all()
        elif type == "S":
            approval_list = Approval.query.filter_by(sender_id=user.id).all()

        ret_json = {
            "success": "true",
            "message": "approval get success",
            "data": approval_list
        }

        return jsonify(ret_json)

    except Exception as e:
        print(e)
        return "False"


@approval_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def approval(id):
    if request.method == "GET":
        try:
            approval = Approval.query.filter_by(id=id).first()
        except Exception as e:
            ret_json = {
                "success": "false",
                "message": "approval db error",
            }

        ret_json = {
            "SUCCESS": "true",
            "message": "approval register success",
            "data": {
                "title": approval.title,
                "content": approval.content,
                "state": approval.state
            }
        }
        return jsonify(ret_json)

@approval_blueprint.route('/', methods=['POST'])
@login_required
def register():
    if request.method == 'POST':
        try:
            user = current_user
            sender_id = request.form['sender_id']
            receiver_id = request.form['receiver_id']
            title = request.form['title']
            content = request.form['content']
            state = 'N'
            last_update_date = datetime.now()

            if user.id != sender_id:
                ret_json = {
                    "success": "false",
                    "message": "로그인 user id와 일치하지 않습니다",
                    "data": {
                        "user_id": id
                    }
                }
                return jsonify(ret_json)

            new_approval = Approval(title, content, current_user.id, current_user.id)
            db.session.add(new_approval)
            db.session.commit()

            return redirect(url_for('index'))

        except IntegrityError:
            db.session.rollback()

        return redirect(url_for('index'))

    user = current_user
    print(user)

    return render_template('register_approval.html')


