# IMPORTS
from flask import render_template, Blueprint, request, redirect, \
    url_for, flash, Markup, abort, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime, timedelta

from app import app, db
from app.document.models import Document
import sys
import traceback
from werkzeug.exceptions import NotFound

import requests
import json


# CONFIG
document_blueprint = Blueprint('document', __name__, template_folder='templates', url_prefix='/document')


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


@document_blueprint.route('', methods=['GET', 'POST'])
@login_required
def documents():
    if request.method == "GET":
        try:
            doc_arr = []
            user_id = current_user.id
            doc_type = request.json.get('doc_type')
            trans = request.json.get('trans')
            page = request.json.get('page')
            count = request.json.get('count')
            status = request.json.get('status')

            if (doc_type is None) or (trans is None) or (page is None) \
                or (count is None) or (status is None):
                ret_json = {
                    "success": "false",
                    "message": "incorrect arguments"
                }
                return jsonify(ret_json)

            if trans == 'S':
                print("test1")
                doc_result = Document.query.filter_by(doc_type=doc_type, status=status, sender_id=user_id)\
                    .paginate(page=int(page), per_page=int(count))
                print("test2")
                document_list = doc_result.items
                has_next = doc_result.has_next
            elif trans == 'R':
                doc_result = Document.query.filter_by(doc_type=doc_type, status=status, receiver_id=user_id)\
                    .paginate(page=int(page), per_page=int(count))
                document_list = doc_result.items
                has_next = doc_result.has_next

            for document in document_list:
                doc_arr.append(row2dict(document))

            ret_json = {
                "success": "true",
                "message": "data",
                "has_next": has_next,
                "data": doc_arr
            }

            return jsonify(ret_json)
        except NotFound as e:
            traceback.print_exc()
            ret_json = {
                "success": "false",
                "message": "page not exist"
            }
            return jsonify(ret_json), 404
        except Exception as e:
            traceback.print_exc()
            ret_json = {
                "success": "false",
                "message": "get document failed",
            }
            return jsonify(ret_json)

    elif request.method == "POST":
        try:
            title = request.json.get('title')
            content = request.json.get('content')
            doc_type = request.json.get('doc_type')
            status = 'W'
            last_update_date = datetime.now()
            # receiver_id = request.form['receiver_id']
            if (title is None) or (content is None) or (doc_type is None):
                ret_json = {
                    "success": "false",
                    "message": "incorrect arguments"
                }
                return jsonify(ret_json)

            # new_document = Document(title, content, current_user.id, receiver_id)
            new_document = Document(title, content, doc_type, current_user.id, current_user.id)
            db.session.add(new_document)
            db.session.commit()

            ret_json = {
                "success": "true",
                "message": "insert document success",
            }
            return jsonify(ret_json)

        except IntegrityError:
            db.session.rollback()
            ret_json = {
                "success": "false",
                "message": "insert document failed"
            }
            return jsonify(ret_json)


@document_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def document(id):
    document = Document.query.filter_by(id=id).first()
    if document is None:
        ret_json = {
            "success": "false",
            "message": "id not exist",
        }
        return jsonify(ret_json), 404

    if request.method == "GET":
        doc_arr = []
        doc_arr.append(row2dict(document))

        ret_json = {
            "success": "true",
            "message": "data",
            "data": doc_arr
        }

        return jsonify(ret_json)

    elif request.method == "PUT":
        try:
            title = request.json.get('title')
            content = request.json.get('content')
            doc_type = request.json.get('doc_type')
            status = request.json.get('status')
            last_update_date = datetime.now()

            if (title is None) or (content is None) or (doc_type is None)\
               or (status is None):
                ret_json = {
                    "success": "false",
                    "message": "incorrect arguments"
                }
                return jsonify(ret_json)

            document.title = title
            document.content = content
            document.doc_type = doc_type
            document.status = status
            document.last_update_date = last_update_date


            db.session.commit()

            ret_json = {
                "success": "true",
                "message": "update document success",
            }
            return jsonify(ret_json)

        except IntegrityError:
            db.session.rollback()
            ret_json = {
                "success": "false",
                "message": "insert document failed"
            }
            return jsonify(ret_json)

    elif request.method == "DELETE":
        try:
            db.session.delete(document)
            db.session.commit()
            ret_json = {
                "success": "false",
                "message": "document delete success",
            }
            return jsonify(ret_json)
        except Exception as e:
            ret_json = {
                "success": "false",
                "message": "document delete failed"
            }
            return jsonify(ret_json)


@document_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'GET':
        return render_template('register_document.html')


@document_blueprint.route('/standby', methods=['GET'])
@login_required
def standby():
    if request.method == "GET":
        try:
            count = Document.query.filter_by(receiver_id=current_user.id).count()
            ret_json = {
                "success": "true",
                "message": "standby",
                "data": count
            }

            return jsonify(ret_json)
        except Exception as e:
            ret_json = {
                "success": "false",
                "message": "standby",
            }
            return jsonify(ret_json)


@document_blueprint.route('/complete', methods=['GET'])
@login_required
def complete():
    if request.method == 'GET':
        try:
            count = Document.query.filter_by(state='Y', receiver_id=current_user.id)

            ret_json = {
                "success": "true",
                "message": "get recent document success",
                "data": count
            }

            return jsonify(ret_json)

        except Exception as e:
            ret_json = {
                "success": "false",
                "message": "get recent document failed"
            }

            return jsonify(ret_json)


@document_blueprint.route('/recent', methods=['GET'])
@login_required
def recent():
    if request.method == 'GET':
        try:
            dict_arr = []
            approval = Document.query.filter_by(doc_type='approval').order_by(Document.regdate).first()
            reflection = Document.query.filter_by(doc_type='reflection').order_by(Document.regdate).first()
            memorandum = Document.query.filter_by(doc_type='memorandum').order_by(Document.regdate).first()
            if approval is not None:
                dict_arr.append(row2dict(approval))
            if reflection is not None:
                dict_arr.append(row2dict(reflection))
            if memorandum is not None:
                dict_arr.append(row2dict(memorandum))
            print(dict_arr)

            ret_json = {
                "success": "true",
                "message": "get recent data success",
                "data": dict_arr
            }

            return jsonify(ret_json)

        except Exception as e:
            print(e)
            ret_json = {
                "success": "false",
                "message": "get recent data failed"
            }
            return jsonify(ret_json)

