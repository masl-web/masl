from flask import Flask, render_template, request, url_for, redirect, jsonify
import maslAreaSelector
import time

app = Flask(__name__)


# 초기 접속 페이지
@app.route('/')
def init_page():
    return render_template('index.html')

# 유저 정보 입력 페이지
@app.route('/userinfo', methods=('GET', 'POST'))
def salary():
    if request.method == 'POST':
        address = request.form['address'] # 직장 주소f
        store_list = request.form.getlist('store') # 매장 선택 정보
        print(address)
        print(store_list)
        area = maslAreaSelector.maslAreaSelector(address)
        result = maslAreaSelector.areaTop10(store_list, area, address)
        return render_template('home.html',area_list=result)
    else:
        return render_template('userinfo.html')

@app.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug = True)