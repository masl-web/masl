import pymongo
import pandas as pd
from haversine import haversine
import json
import requests

# Docker 환경에서 MongoDB 연결 설정
masl_client = pymongo.MongoClient(host='host.docker.internal', port=27017)

db = masl_client['LocationData']
store_col = db['StoreData']
metro_col = db['MetroData']
bus_stop_col = db['BusStopData']
bus_lines_col = db['BusLinesData']
env_col = db['EnvironmentData']
'''
# 위/경도로 행정지역명 반환하는 함수
def regionName(lat, lng):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?{}'.format("x={0}&y={1}".format(lng, lat))
    headers = {"Authorization": "KakaoAK 6f3c5c2ae909068ed7155b2e79237b82"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    regal_region = result['documents'][1]['region_2depth_name']
    return regal_region

# 지하철 CSV 데이터 MongoDB에 적재
metro = pd.read_csv('BackData/metro_station_seoul_final.csv', encoding='cp949')
count = 1
for i in range(0,443):
    print(count/443)
    count += 1
    if " " not in metro.loc[i][1]:
        pass
    else:
        metro_col.insert({"type": "지하철역", "line": metro.loc[i][1].split(" ")[1],
            "station_name": metro.loc[i][1].split(" ")[0], "station_address": metro.loc[i][2],
            "geo_lat": metro.loc[i][3], "geo_lng": metro.loc[i][4],
            "region_name": regionName(metro.loc[i][3], metro.loc[i][4])})

# 버스정류장 CSV 데이터 MongoDB에 적재
bus_stop = pd.read_csv('BackData/bus_stop_seoul_final.csv', encoding='cp949')
bus_lines = pd.read_csv('BackData/bus_line_seoul_final.csv', encoding='utf-8')
for i in range(0,11178):
    temp_list= bus_lines[bus_lines["정류소ID"] == (int(bus_stop.loc[i][2]))]["노선명"].values.tolist()
    bus_stop_col.insert({"type": "버스정류소", "station_name": bus_stop.loc[i][1], "station_id": str(bus_stop.loc[i][2]), 
        "geo_lat": bus_stop.loc[i][4], "geo_lng": bus_stop.loc[i][5], 
        "region_name": regionName(bus_stop.loc[i][4], bus_stop.loc[i][5]), 
        "bus_line": temp_list })
'''
# 버스노선 CSV 데이터 MongoDB에 적재
bus_lines = pd.read_csv('BackData/bus_line_seoul_final.csv')
for i in range(0,39362):
    bus_lines_col.insert({"station_id": int(bus_lines.loc[i][4]), "bus_line": str(bus_lines.loc[i][1])})
'''
# 매장 CSV 데이터 MongoDB에 적재
store_files = [
    '0323_angelinus_seoul.csv',
    '0323_burgerking_seoul.csv',
    '0323_coffeebean_seoul.csv',
    '0323_cu_seoul.csv',
    '0323_emart_seoul.csv',
    '0323_emart24_seoul.csv',
    '0323_gongcha_seoul.csv',
    '0323_gs25_seoul.csv',
    '0323_hollys_seoul.csv',
    '0323_homeplus_seoul.csv',
    '0323_issactoast_seoul.csv',
    '0323_lalabla_seoul.csv',
    '0323_lobs_seoul.csv',
    '0323_lottemart_seoul.csv',
    '0323_lotteria_seoul.csv',
    '0323_mcdonalds_seoul.csv',
    '0323_ministop_seoul.csv',
    '0323_oliveyoung_seoul.csv',
    '0323_paulbassette_seoul.csv',
    '0323_seveneleven_seoul.csv',
    '0323_starbucks_seoul.csv',
    '0323_subway_seoul.csv'
]
for file in store_files:
    store = pd.read_csv('BackData/'+file, encoding='utf-8')
    for i in range(len(store)):
        store_col.insert(dict({"type": store.loc[i][2], "brand": store.loc[i][3], "store_name": store.loc[i][4], "store_address": store.loc[i][5], 
            "geo_lat": store.loc[i][6], "geo_lng": store.loc[i][7]}))

# 시설 CSV 데이터 MongoDB에 적재
env_col.insert({"type": "공원", "name": "서초2동주민센터", "address": "서울 서초구 서초대로70길 51", "geo_lat": 37.4920694663699, "geo_lng": 127.024947759276})
# env_col.createIndex({"address":"text"})
'''