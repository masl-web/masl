import json
import requests
import pymongo
from haversine import haversine
from operator import itemgetter
import livecrawler
import time


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


# 주소 >> 위성좌표값 반환(KakaoMap)
def getGeoCode(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format(address)
    headers = {"Authorization": "KakaoAK db80de33bb89c7f47c6cb2948ca14e90"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    if result['documents'] == []:
        return "-", "-"
    else:
        match_first = result['documents'][0]['address']
        return float(match_first['y']), float(match_first['x'])

# User가 입력한 [회사/학교/기타] 주소 0.5km 내에 있는 지하철 역 리스트 stations 반환
def nearMetro(home):
    stations = []
    for m in metro_col.find():
        if haversine(home, (m['geo_lat'],m['geo_lng'])) <= 0.5: # haversine 함수는 두 위성좌표의 거리를 알려준다. 단위는 km이다.
            if m['station_name'] not in stations:
                stations.append(m['station_name'])
    if len(stations) == 0:
        stations = None
        
    else:
        return stations

# nearMetro 함수에서 반환된 stations를 지나는 모든 지하철 노선 리스트 lines 반환
def getMetroLine(stations):
    if stations != None:
        lines = []
        for station in stations:
            for m in metro_col.find({"station_name": station}):
                if m['line'] not in lines:
                    lines.append(m['line'])
    return lines

# nearMetro 함수에서 반환된 lines가 지나는 모든 지하철 역 리스트 all_metro_stations 반환
def allMetroLineStations(lines):
    all_metro_station = []
    allStationName = []
    for line in lines:
        for m in metro_col.find({"line": line}):
            if m['station_name'] not in allStationName:
                temp = []
                temp.append(m['station_name'])
                temp.append(m['geo_lat'])
                temp.append(m['geo_lng'])
                all_metro_station.append(temp)
                allStationName.append(m['station_name'])
    return all_metro_station

# User가 입력한 [회사/학교/기타] 주소 0.2km 내에 있는 지하철 역 리스트 stations 반환
def nearBusStop(home):
    bus_stop = []
    for b in bus_stop_col.find():
        if haversine(home, (b['geo_lat'],b['geo_lng'])) <= 0.2: # haversine 함수는 두 위성좌표의 거리를 알려준다. 단위는 km이다.
            if b['station_id'] not in bus_stop:
                bus_stop.append(b['station_id'])
    if len(bus_stop) == 0:
        return None
    else:
        return bus_stop

# nearBusStop 함수에서 반환된 bus_stop 리스트를 지나는 모든 버스 노선 리스트 bus_line 반환
def allBusLine(bus_stop):
    bus_line = []
    for s in bus_stop:
        for l in bus_lines_col.find():
            if int(s) == l['station_id']:
                bus_line.append(l['bus_line'])
    return bus_line

# allBusLine 함수에서 반환된 bus_line 리스트의 버스 노선이 지나는 모든 버스 정류장 리스트 all_bus_stop 반환
def allBusStop(bus_line):
    all_bus_stop = []
    count = []
    for l in bus_line:
        for b in bus_lines_col.find():
            if l == b['bus_line']:
                temp = []
                if b['station_id'] not in count:
                    count.append(b['station_id'])
                    temp.append(b['station_id'])
                    query = {"station_id": str(b['station_id'])}
                    for x in bus_stop_col.find(query):
                        temp.append(x['geo_lat'])
                        temp.append(x['geo_lng'])
                    if len(temp) ==3:
                        all_bus_stop.append(temp)
    return all_bus_stop

# MASL 1차 탐색 대상 지역 추출 함수, 결과값으로 data 리스트 반환
def maslAreaSelector(address):
    home = getGeoCode(address)
    if home[0] != str:
        bus_stop = nearBusStop(home)
        if bus_stop != None:
            bus_line = allBusLine(bus_stop)
            all_bus_stop = allBusStop(bus_line)
            stations = nearMetro(home)
            if stations != None:
                lines = getMetroLine(stations)
                all_metro_station = allMetroLineStations(lines)
                data = all_metro_station + all_bus_stop
                return data
            else:
                data = all_bus_stop
                return data
        else:
            stations = nearMetro(home)
            if stations != None:
                lines = getMetroLine(stations)
                all_metro_station = allMetroLineStations(lines)
                data = all_metro_station
                return data
    else:
        return None


# maslAreaSelector 함수에서 반환된 data 리스트 중 User가 선택한 매장이 밀집한 지역과 거리를 기준으로 TOP10 지역 리스트 data 반환 (거리 알고리즘 개선 필요)
def areaTop10(brand, data_l, address):
    home = getGeoCode(address)
    query = {"brand": {"$in": brand}}
    for s in store_col.find(query):
        for i in range(0, len(data_l)):
            if haversine([data_l[i][1],data_l[i][2]],[s["geo_lat"],s["geo_lng"]]) <= 0.5:
                if len(data_l[i]) == 3:
                    data_l[i].append(1)
                elif len(data_l[i]) == 4:
                    data_l[i][3] += 1
            elif len(data_l[i]) == 3:
                data_l[i].append(0)
    for d in data_l:
        d[3] = d[3] + 20 - haversine(home, [d[1],d[2]])
    data_l.sort(key=itemgetter(3), reverse=True)
    data_l = data_l[:5] # 임시로 5개만 출력
    result = {
        "area1": (data_l[0][1],data_l[0][2]),
        "area2": (data_l[1][1],data_l[1][2]),
        "area3": (data_l[2][1],data_l[2][2]),
        "area4": (data_l[3][1],data_l[3][2]),
        "area5": (data_l[4][1],data_l[4][2]),
        }
    
    return result

def searchTop10(data):
    search_keyword = ['병원', '은행', '동사무소']
    for i in data:
        url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?{}'.format("x={0}&y={1}".format(i[2],i[1]))
        headers = {"Authorization": "KakaoAK db80de33bb89c7f47c6cb2948ca14e90"}
        result = json.loads(str(requests.get(url, headers=headers).text))
        regal_area = result['documents'][1]['address_name']
        regal_region = result['documents'][1]['region_2depth_name']
        print("1")
        if env_col.find({"$text":{"$search": regal_region}}).count() == 0:
            print("2")
            for keyword in search_keyword:
                print("3")
                livecrawler.area_crawler(regal_area, keyword)
                time.sleep(4)
                print("4")



        



address = '서울시 서초구 서초중앙로 65'
brand = ["starbucks", "맥도날드"]
data = maslAreaSelector(address)
result = areaTop10(brand, data, address)
print(result)




