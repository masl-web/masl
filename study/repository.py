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

@app.errorhandler(404) 
def page_not_found(error):
    return "<h1>404 Error</h1>", 404
# 없는 페이지를 요청했을 때의 에러

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('jinjatest.html', name=user)
#데이터 전달하기

