from flask import Flask, jsonify, request, render_template, make_response
from view import blog
import requests

app = Flask(__name__, static_url_path='/static')
# Flask 객체를 app에 할당

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')

@app.route('/')
def test():
    return render_template('index.html')
#라우팅을 통해 URL을 해당 URL에 맞는 기능과 연결해 줌

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('jinjatest.html', name=user)
#데이터 전달하기

@app.errorhandler(404) 
def page_not_found(error):
    return "<h1>404 Error</h1>", 404
# 없는 페이지를 요청했을 때의 에러

@app.route('/hello_if')
def hello_html():
    value = 27
    return render_template('condition.html', data=value)
#조건문 테스트

@app.route("/google")
def get_google():
    response = requests.get("http://www.google.co.kr")
    return response.text 
#크롤링 테스트

@app.route('/login')
def login():
    username = request.args.get('user_name')
    passwd = request.args.get('passwd')
    if username == 'ksy' and passwd == '9926':
        return_data = {'auth':'success'}
    else:
        return_data = {'auth':'failed'}
    return jsonify(return_data)
#/login?user_name=ksy&passwd=9926 입력시 success

if __name__=='__main__':
    app.run(host = '127.0.0.1', port = '5001', debug=True)
#웹 서버 구동. 직접 실행시만 실행. 안될시 포트번호 바꿔보기