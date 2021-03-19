from flask import Flask, render_template, request, url_for, redirect, jsonify
import time
from flask_cors import CORS
import json
import requests
import pymongo
from haversine import haversine
from operator import itemgetter

from maslAreaSelector import maslAreaSelector, areaTop10

app = Flask(__name__)

CORS(app, supports_credentials=True)

# 초기 접속 페이지
@app.route('/')
def init_page():
    return render_template('index.html')

# 유저 정보 입력 페이지
@app.route('/userinfo', methods=['GET', 'POST'])
def salary():
    if request.method == 'POST':
        userInfo = request.get_json() 
        address = userInfo.get('address')# 직장 주소f
        store_list = userInfo.get('brand') # 매장 선택 정보
        print(address)
        print(store_list)
        start_time = time.time()
        area = maslAreaSelector(address)
        result = areaTop10(store_list, area, address)
        print('걸린시간: ', time.time() - start_time)
        return jsonify(areaList = result)
        # return render_template('home.html',area_list=result)
    # elif request.method == 'GET':
        # return jsonify(areaList = result)
        # return render_template('Userinfo.html')
    # else:
    return jsonify(err = "err")

@app.route('/masl', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port='5000', debug = True)
