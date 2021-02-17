from flask import Flask, render_template, request, url_for, redirect, jsonify
import maslAreaSelector

app = Flask(__name__)

# @app.route('/')
# def test():
#         return render_template('map.html')

# 초기 접속 페이지
@app.route('/')
def init_page():
    return render_template('index.html')

# 유저 정보 입력 페이지
@app.route('/UserInfo', methods=('GET', 'POST'))
def salary():
    if request.method == 'POST':
        address = request.form['address'] # 직장 주소
        store_list = request.form.getlist('store') # 매장 선택 정보
        print(address)
        print(store_list)
        area = maslAreaSelector.maslAreaSelector(address)
        result = maslAreaSelector.areaTop10(store_list, area, address)
        print(result)
        return render_template('home.html',area_list=result)
    return render_template('Userinfo.html')

@app.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug = True)
