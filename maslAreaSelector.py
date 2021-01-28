import json
import requests
import pymongo
from haversine import haversine
import pandas as pd



masl_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = masl_client['LocationData']
store_col = db['StoreData']
metro_col = db['MetroData']
bus_stop_col = db['BusStopData']
bus_lines_col = db['BusLinesData']

def getGeoCode(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format(address)
    headers = {"Authorization": "KakaoAK db80de33bb89c7f47c6cb2948ca14e90"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    if result['documents'] == []:
        return "-", "-"
    else:
        match_first = result['documents'][0]['address']
        return float(match_first['y']), float(match_first['x'])


def NearMetro(home):
    stations = []
    for m in metro_col.find():
        if haversine(home, (m['geo_lat'],m['geo_lng'])) <= 0.5:
            if m['station_name'] not in stations:
                stations.append(m['station_name'])
    if len(stations) == 0:
        print("주변에 지하철 역이 없음")
    else:
        return stations

def getMetroLine(stations):
    lines = []
    for station in stations:
        for m in metro_col.find({"station_name": station}):
            if m['line'] not in lines:
                lines.append(m['line'])
    return lines

def allMetroLineStations(lines):
    all_metro_station = []
    for line in lines:
        allStationName = []
        allStationInfo = []
        for m in metro_col.find({"line": line}):
            if m['station_name'] not in allStationName:
                temp = []
                temp.append(m['station_name'])
                temp.append(m['geo_lat'])
                temp.append(m['geo_lng'])
                allStationInfo.append(temp)
                allStationName.append(m['station_name'])
        all_metro_station.append(allStationInfo)
    return all_metro_station

def nearBusStop(home):
    bus_stop = []
    for b in bus_stop_col.find():
        if haversine(home, (b['geo_lat'],b['geo_lng'])) <= 0.1:
            if b['station_id'] not in bus_stop:
                bus_stop.append(b['station_id'])
    if len(bus_stop) == 0:
        print("주변에 버스정류장이 없음")
    else:
        return bus_stop

def allBusLine(bus_stop):
    bus_line = []
    for s in bus_stop:
        for l in bus_lines_col.find():
            if int(s) == l['station_id']:
                bus_line.append(l['bus_line'])
    return bus_line

def allBusStop(bus_line):
    all_bus_stop = []
    for l in bus_line:
        for b in bus_lines_col.find():
            if l == b['bus_line']:
                temp = []
                temp.append(b['station_id'])
                query = {"station_id": str(b['station_id'])}
                for x in bus_stop_col.find(query):
                    temp.append(x['geo_lat'])
                    temp.append(x['geo_lng'])
                if len(temp) ==3:
                    all_bus_stop.append(temp)
    return all_bus_stop

address = '서울시 서초구 서초중앙로 65'
home = getGeoCode(address)
bus_stop = nearBusStop(home)
bus_line = allBusLine(bus_stop)
all_bus_stop = allBusStop(bus_line)
stations = NearMetro(home)
lines = getMetroLine(stations)
all_metro_station = allMetroLineStations(lines)
data = all_metro_station + all_bus_stop
brand = ['starbucks',"세븐일레븐","올리브영","맥도날드","GS25","CU"]

def storeSearch(brand, data):
    result = []
    for b in brand:
        query = {"brand": b}
        for s in store_col.find(query):
            lat = s['geo_lat']
            lng = s['geo_lng']
            for d in data:
                if type(d[1]) == float and type(d[2]) == float:
                    if haversine([float(d[1]), float(d[2])],[float(lat), float(lng)]) <= 0.5:
                        temp = {}
                        temp['area_lat'] = d[1]
                        temp['area_lng'] = d[2]
                        temp['store_name'] = s['store_name']
                        temp['store_address'] = s['store_address']
                        temp['store_lat'] = lat
                        temp['store_lng'] = lng
                        if len(temp) == 6:
                            result.append(temp)
    return result

def areaScoreForTop10(result):
    count = []
    target = []
    for r in result:
        temp = []
        temp.append(r['area_lat'])
        temp.append(r['area_lng'])
        if temp not in target:
            count.append(temp)
            temp.append(1)
            target.append(temp)
        elif temp in count:
            for t in target:
                if t[:2] == temp:
                    t[2] = t[2] + 1
    for t in target:
        t = t.append(haversine(home,[t[0],t[1]]))
    df = pd.DataFrame(target)
    return df




result = storeSearch(brand, data)
target = areaScoreForTop10(result)
print(target)
