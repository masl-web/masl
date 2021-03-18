from flask import Flask, render_template, request, url_for, redirect, jsonify
import time
from flask_cors import CORS
import json
import requests
import pymongo
from haversine import haversine
from operator import itemgetter

import maslAreaSelector

app = Flask(__name__)

CORS(app, supports_credentials=True)

# MongoDB 연결 (localhost:27017은 default, 추후 변경)
masl_client = pymongo.MongoClient('mongodb://localhost:27017/')

# MASL용 데이터베이스 LocationData 생성
db = masl_client['LocationData']

# 필요 Collection 생성(스토어정보:StoreData / 지하철정보:MetroData / 버스정류장정보:BusStopData / 버스노선정보:BusLineData)
store_col = db['StoreData']         # DB구조 : {"type": [], "brand": [], "store_name": [지점명], "store_address": [], "geo_lat": [], "geo_lng": []}
metro_col = db['MetroData']         # DB구조 : {"type": "Metro", "line": [], "station_name": [], "station_address": [], "geo_lat": [], "geo_lng": []}
bus_stop_col = db['BusStopData']    # DB구조 : {"type": "BusStop", "station_name": [], "station_id": [정류장고유번호], "geo_lat": , "geo_lng": []}
bus_lines_col = db['BusLinesData']  # DB구조 : {"station_id": [정류장고유번호], "bus_line": []}
env_col = db['EnvironmentData']     # DB구조 : {"type": [], "name": [], "address": [], "geo_lat": [], "geo_lng": []}

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
    if request.method == 'GET':
        return jsonify(areaList = result)
        # return render_template('Userinfo.html')
    else:
        return jsonify(err = "err")

@app.route('/masl', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port='5000', debug = True)

