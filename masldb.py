import pymongo
import pandas as pd
from haversine import haversine
import json
import requests

masl_client = pymongo.MongoClient('mongodb://localhost:27017/')

db = masl_client['LocationData']
store_col = db['StoreData']
metro_col = db['MetroData']
bus_stop_col = db['BusStopData']
bus_lines_col = db['BusLinesData']
env_col = db['EnvironmentData']

def regionName(lat, lng):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?{}'.format("x={0}&y={1}".format(lng, lat))
    headers = {"Authorization": "KakaoAK 6f3c5c2ae909068ed7155b2e79237b82"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    regal_region = result['documents'][1]['region_2depth_name']
    return regal_region

# 지하철 역 csv 파일 몽고db에 초기 값으로 저장
if metro_col.find({}) == None:
    metro = pd.read_csv('BackData/metro_station_seoul_final.csv', encoding='cp949')
    count = 1
    for i in range(0,443):
        print(count/443)
        count += 1
        if " " not in metro.loc[i][1]:
            pass
        else:
            metro_col.insert({"type": "Metro", "line": metro.loc[i][1].split(" ")[1],
                            "station_name": metro.loc[i][1].split(" ")[0], "station_address": metro.loc[i][2],
                            "geo_lat": metro.loc[i][3], "geo_lng": metro.loc[i][4], "region_name": regionName(metro.loc[i][3], metro.loc[i][4])})

# 버스정류장 csv 파일 몽고db에 초기 값으로 저장
if bus_stop_col.find({}) == None:
    bus_stop = pd.read_csv('BackData/bus_stop_seoul_final.csv', encoding='cp949')
    df = pd.read_csv('BackData/seoul_busline_info.csv', encoding='utf-8')
    for i in range(0,11178):
        temp_list= df[df["정류소ID"] == (int(bus_stop.loc[i][2]))]["노선명"].values.tolist()
        bus_stop_col.insert({"type": "BusStop", "station_name": bus_stop.loc[i][1], "station_id": str(bus_stop.loc[i][2]), 
                        "geo_lat": bus_stop.loc[i][4], "geo_lng": bus_stop.loc[i][5], "region_name": regionName(bus_stop.loc[i][4], bus_stop.loc[i][5]), 
                        "bus_line": temp_list })

if bus_lines_col.find({}) == None:
    bus_lines = pd.read_csv('BackData/seoul_busline_info.csv', encoding='utf-8')
    for i in range(0,39362):
        bus_lines_col.insert({"station_id": bus_lines.loc[i][4], "bus_line": bus_lines.loc[i][1]})

# 스타벅스 csv 파일 몽고db에 초기 값으로 저장
if store_col.find({}) == None:
    store = pd.read_csv('BackData/starbucks_seoul(geo)_final.csv', encoding='cp949')
    for i in range(0,499):
        store_col.insert({"type": "Cafe", "brand": "starbucks", "store_name": store.loc[i][4], "store_address": store.loc[i][5],
                        "geo_lat": store.loc[i][6], "geo_lng": store.loc[i][7]})

if env_col.find({}) == None:
    env_col.insert({"type": "park", "name": "서초2동주민센터", "address": "서울 서초구 서초대로70길 51", "geo_lat": 37.4920694663699, "geo_lng": 127.024947759276})
    env_col.createIndex({"address":"text"})

# db에 매장이름과 매장주소가 없을 시 store 컬렉션에 추가
def addStoreData(store_type, brand, store_name, store_address, geo_lat, geo_lng):
    query = {"$and": [{"store_name": store_name}, {"store_address": store_addr}]}
    if store_col.find(query).count() == 0:
        store_col.insert({"type": store_type,
                        "brand": brand,
                        "store_name": store_name,
                        "store_address": store_address,
                        "geo_lat": geo_lat,
                        "geo_lng": geo_lng})

def addEnvData(env_type, name, address, geo_lat, geo_lng):
    query = {"$and": [{"store_name": name}, {"store_address": address}]}
    if store_col.find(query).count() == 0:
        store_col.insert({"type": env_type,
                        "name": name,
                        "address": address,
                        "geo_lat": geo_lat,
                        "geo_lng": geo_lng})

# db에 해당 브랜드 데이터가 있는 지 조회 / 있다면 스토어 리스트를 없다면 False값 반환
def searchStoreData(target_location, store_type, brand):
    query = {"type": store_type, "brand": brand}
    count = 0
    store_list = []
    for store in store_col.find(query):
        store_location = store['geo_lng'],store['geo_lat']
        if haversine(target_location, store_location) <= 0.5:
            temp = []
            count += 1
            temp.append(store['type'])
            temp.append(store['brand'])
            temp.append(store['store_name'])
            temp.append(store['store_address'])
            temp.append(store['geo_lat'])
            temp.append(store['geo_lng'])
            store_list.append(temp)
    if count > 0:
        return store_list
    else:
        return False


