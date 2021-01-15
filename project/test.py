from flask import Flask, jsonify, request, render_template, make_response
from view import blog
import requests
app = Flask(__name__, static_url_path='/static')
# Flask 객체를 app에 할당
app.register_blueprint(blog.blog_abtest, url_prefix='/blog')

@app.route('/')
def student():
   return render_template('give.html')
#라우팅을 통해 URL을 해당 URL에 맞는 기능과 연결해 줌

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      if result['Area'] not in ['강남', '강북', '강동', '강서'] or result['Distance'] not in ['100m', '250m', '500m', '1km'] or result['Price'] not in ['~50만', '~60만', '~70만', '70만 이상']:
        return render_template("contenterror.html")
      return render_template("result.html",result = result)

@app.route('/result2',methods = ['POST', 'GET'])
def result2():
   if request.method == 'POST':
      result2 = request.form
      return render_template("result2.html")

if __name__=='__main__':
    app.run(host = '127.0.0.1', port = '5001', debug=True)
#웹 서버 구동. 직접 실행시만 실행. 안될시 포트번호 바꿔보기