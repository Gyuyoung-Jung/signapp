# IMPORTS
from flask import render_template, jsonify
from flask_login import LoginManager, current_user
from flask import request
import flask
import datetime
from werkzeug.utils import secure_filename
from app import app


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

from app.user.models import User


@login_manager.user_loader
def load_user(user_id):
    print(flask.session)
    return User.query.filter(User.id == int(user_id)).first()


@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    flask.session.modified = True
    flask.g.user = current_user


# BLUEPRINTS
from app.user.views import user_blueprint
from app.auth.views import auth_blueprint
from app.oauth.views import oauth_blueprint
from app.document.views import document_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(oauth_blueprint)
app.register_blueprint(document_blueprint)


# ROUTES
@app.route('/', methods=['GET', 'POST'])
def index():
    """Render homepage"""
    data = {
        "success": "True",
        "message": "Index Page"
    }
    return jsonify(data)


@app.route('/upload')
def render_file():
    return render_template('upload.html')


@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공!'


# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    data = {
        "success": "false",
        "message": "404 Error"
    }
    print(data)
    return jsonify(data), 404


@app.errorhandler(403)
def page_forbidden(e):
    data = {
        "success": "false",
        "message": "403 Error"
    }
    return jsonify(data)


@app.errorhandler(410)
def page_gone(e):
    data = {
        "success": "false",
        "message": "410 Error"
    }
    return jsonify(data)
