from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
# from flask_cors import CORS
from masl_view import blog
# import os

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
#CORS(app)
app.secure_key = 'temporary_key'
#원래는 랜덤 값이 보안이 좋으나 여기서는 고정 키 사용.

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

@app.route('/')
def test():
    return render_template('index.html')

if __name__=='__main__':
    app.run(host = '127.0.0.1', port = '5000', debug=True)