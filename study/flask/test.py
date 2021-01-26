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

@app.route('/result', methods=['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      correct_area = ['강남', '강북', '강동', '강서']
      correct_distance = ['100m', '250m', '500m', '1km']
      correct_price = ['~50만', '~60만', '~70만', '70만 이상']

      check_area = result['Area'] not in correct_area
      check_distance = result['Distance'] not in correct_distance
      check_price = result['Price'] not in correct_price

      if check_area or check_distance or check_price:
        return render_template("contenterror.html")
      return render_template("result.html",result = result)

@app.route('/result2', methods=['POST', 'GET'])
def result2():
   if request.method == 'POST':
      result2 = request.form
      return render_template("result2.html")

if __name__=='__main__':
    app.run(debug=True)
#linux환경에서 실행 시 아래 코드를 입력
#5000포트 사용시 제 컴퓨터 환경에서는 실행이 안되서 우선 8080포트 사용했습니다.
# export FLASK_APP=test.py
# export FLASK_RUN_HOST=127.0.0.1
# export FLASK_RUN_PORT=8080
# flask run