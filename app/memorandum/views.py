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
memorandum_blueprint = Blueprint('memorandum', __name__, template_folder='templates', url_prefix='/memorandum')


@memorandum_blueprint.route('/list', methods=['GET'])
@login_required
def list():
    try:
        #type = request.args.get('type')
        type = 'R'
        user = current_user

        if type == "R":
            approval_list = Approval.query.filter_by(receiver_id=user.id).all()
        elif type == "S":
            approval_list = Approval.query.filter_by(sender_id=user.id).all()

        return "True"

    except Exception as e:
        print(e)
        return "False"


@memorandum_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            state = 'N'
            last_update_date = datetime.now()
            # receiver_id = request.form['receiver_id']

            # new_approval = Approval(title, content, current_user.id, receiver_id)
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


