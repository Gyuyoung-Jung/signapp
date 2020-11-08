# IMPORTS
from flask import render_template, Blueprint, request, redirect, \
    url_for, flash, Markup, abort, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime, timedelta

from app import app, db
from app.reflection.models import Reflection

import requests
import json


# CONFIG
auth_blueprint = Blueprint('approval', __name__, template_folder='templates', url_prefix='/approval')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        result = {}
        # nid = request.form['nid']
        # email = request.form['email']
        nid = request.args.get('nid')
        email = request.args.get('email')
        user = User.query.filter_by(nid=nid, email=email).first()
        if user is not None:
            # user.authenticated = True
            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()
            login_user(user)
            message = Markup(
                "<strong>Welcome back!</strong> You are now successfully logged in.")
            flash(message, 'success')

            result = {
                'resultcode': '00',
                'message': 'success',
                'response': {
                    'nid': nid,
                    'email': email,
                }
            }

            print(result)

            # return redirect(url_for('index'))
            return jsonify(result)
        else:
            message = Markup(
                "<strong>Error!</strong> Incorrect login credentials.")
            flash(message, 'danger')
            return "False"

    return redirect(url_for('index'))


