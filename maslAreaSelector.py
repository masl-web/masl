import json
import requests
import pymongo
from haversine import haversine
from operator import itemgetter
import time
import pandas as pd

check_time = time.time()

# MongoDB 연결 (localhost:27017은 default, 추후 변경)
# masl_client = pymongo.MongoClient(host='host.docker.internal', port=27017)
# masl_client = pymongo.MongoClient('mongodb://localhost:27017/')
masl_client = pymongo.MongoClient('mongodb://masl:masl_dev@localhost:27017/')

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

    # KAKAO REST API 토큰 인증 - 2021/3/9 21:00 신규 등록
    headers = {"Authorization": "KakaoAK 6f3c5c2ae909068ed7155b2e79237b82"}

    # url 로 위경도 정보 호출
    result = json.loads(str(requests.get(url, headers=headers).text))

    # 위경도 정보 호출 실패 시 위도 경도 값 각각 "-" 값으로 대체
    if result['documents'] == []:
        return "-", "-"
    else:
        match_first = result['documents'][0]['address']
        # y 좌표(위도), x 좌표(경도) 반환
        return float(match_first['y']), float(match_first['x'])
# 위성좌표값 >> 행정구역 반환(KakaoMap)
def regionName(lat, lng):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?{}'.format("x={0}&y={1}".format(lng, lat))
    headers = {"Authorization": "KakaoAK 6f3c5c2ae909068ed7155b2e79237b82"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    regal_region = result['documents'][1]['address_name']
    return regal_region

# 행정구역에 따른 점수 반환(가격이 높은 강남구는 낮게, 가격이 낮은 도봉구는 높게)
def regionScore(region_name):
    # 서울 원룸 평균 월세
    region_dict = {
        '강남구':66, '강동구':45, '강북구':41, '강서구':39,
        '관악구':41, '광진구':50, '구로구':38, '금천구':35,
        '노원구':37, '도봉구':32, '동대문구':44, '동작구':45,
        '마포구':54, '서대문구':43, '서초구':61, '성동구':50,
        '성북구':45, '송파구':53, '양천구':44, '영등포구':43,
        '용산구':47, '은평구':40, '종로구':50, '중구':54,
        '중랑구':43
    }
    if region_name not in region_dict:
        score = -100
    else: 
        score = region_dict[region_name]
        score = abs(66/score)**5
    return score


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
                temp.append(m['region_name'])
                all_metro_station.append(temp)
                allStationName.append(m['station_name'])
    return all_metro_station

# User가 입력한 [회사/학교/기타] 주소 0.2km 내에 있는 지하철 역 리스트 stations 반환
def nearBusStop(home):
    bus_stop = []
    for b in bus_stop_col.find():
        if haversine(home, (b['geo_lat'],b['geo_lng'])) <= 0.2: # haversine 함수는 두 위성좌표의 거리를 알려준다. 단위는 km이다.
            if b['station_id'] not in bus_stop:  # bus_stop = [강남버스정류장, 선릉버스정류장, ... 정류장]
                bus_stop.append(b['station_id'])
    if len(bus_stop) == 0:
        return None
    else:
        print("Bus Stop:", bus_stop)
        return bus_stop

# nearBusStop 함수에서 반환된 bus_stop 리스트를 지나는 모든 버스 노선 리스트 bus_line 반환
def allBusLine(bus_stop):  
    bus_line = []
    for s in bus_stop:  # bus_stop: ['122000174', '122000202', '122000602', '122000603', '122000721']
        query = {"station_id": int(s)}
        for line in bus_lines_col.find(query):
            bus_line.append(line['bus_line'])
    print('bus_line:', bus_line)
    return set(bus_line)

# allBusLine 함수에서 반환된 bus_line 리스트의 버스 노선이 지나는 모든 버스 정류장 리스트 all_bus_stop 반환
def allBusStop(bus_lines):
    all_bus_stop = []
    check_station = []
    for bus_line in bus_lines: # bus_lines : {'360', '6000', '146', '341', 'N13', '740', '6703', 'N61'}    
        query = {"bus_line": {'$in':[bus_line]}}
        for row in bus_stop_col.find(query): # 버스노선이 지나는 모든 버스정류장
            if row['station_id'] not in check_station:
                check_station.append(row['station_id'])
                all_bus_stop.append([int(row['station_id']), row['geo_lat'], row['geo_lng'], row['region_name']])
    # print('all_bus_stop:', all_bus_stop)
    print('all_bus_stop 길이:', len(all_bus_stop))
    return all_bus_stop  # [[123000605, 37.4693007674, 127.13153855030001, '송파구'] [], ...[]] 

# MASL 1차 탐색 대상 지역 추출 함수, 결과값으로 data 리스트 반환
def maslAreaSelector(address):
    home = getGeoCode(address)  # 위도, 경도 반환
    print('회사 위치: ', home) # 위성좌표 잘 반환함
    if home[0] != str:
        bus_stop = nearBusStop(home)
        
        if bus_stop != None:
            bus_line = allBusLine(bus_stop)

            start = time.time()
            all_bus_stop = allBusStop(bus_line)
            print('allBusStop 시간: ', time.time() - start)

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
    brand_score = []
    distance_score = []
    price_score = []
    home = getGeoCode(address)
    # print('data_l:', data_l)
    for b in brand:
        if b == '':
            brand.remove(b)
    for i in range(0, len(data_l)):
        if len(data_l[i]) == 4:
            data_l[i].insert(0, [])
        query = {"$and": 
                [{"brand": {"$in": brand}}, 
                {"$and": [{"geo_lat": {"$lte": data_l[i][2]+0.009}}, {"geo_lat": {"$gte": data_l[i][2]-0.009}}]},
                {"$and": [{"geo_lng": {"$lte": data_l[i][3]+0.009}}, {"geo_lng": {"$gte": data_l[i][3]-0.009}}]}
                ]}
        for s in store_col.find(query):
            # start = time.time()
            # x = s['geo_lat'] - data_l[i][2]
            # y = s['geo_lng'] - data_l[i][3]
            # r = (x**2 + y**2)**0.5
            # print('r 값:', r)
            # print('r 시간:', time.time() - start)

            # start = time.time()
            # hs = haversine([data_l[i][2],data_l[i][3]],[s["geo_lat"],s["geo_lng"]])
            # print('hs 값:', hs)
            # print('hs 시간:', time.time() - start)

            if haversine([data_l[i][2],data_l[i][3]],[s["geo_lat"],s["geo_lng"]]) <= 0.5:
                if s['brand'] in data_l[i][0]:
                    pass
                else:
                    data_l[i][0].append(s['brand'])

    for data in data_l:
        data[0] = len(data[0])
        # 서울이 아닌 지역이 나오는 경우
        if regionScore(data[4]) == -100:
            data[0] = 0
        else:
            # 브랜드점수, 거리점수, 월세점수 넣어주기
            brand_score.append(round(data[0]*20/len(brand), 2))
            data[0] = [data[0]*20/len(brand), 11 - ((haversine(home, (data[2], data[3])))/11)**2,regionScore(data[4])/2]
            distance_score.append(round(11 - ((haversine(home, (data[2], data[3])))/11)**2 ,2))
            price_score.append(round(regionScore(data[4])/2, 2))
        
    # 브랜드점수(1~20), 거리점수(1~20), 월세점수(1~20) 이 되도록 알파값 구해서 곱해주기
    brand_alpha = 21/(max(brand_score) - min(brand_score)+1)
    distance_alpha =  21/(max(distance_score) - min(distance_score)+1)
    price_alpha =  21/(max(price_score) - min(price_score)+1)

    for data in data_l:
        if type(data[0]) != int:
            data[0] = data[0][0]*brand_alpha + data[0][1]*distance_alpha + data[0][2]*price_alpha
    data_l.sort(key=itemgetter(0), reverse=True)
    result_list = []
    result_list.append(data_l[0])

    # 근접거리가 3km 이하인 지역을 제외
    for i in range(1, len(data_l)):
        temp = 0
        for r in result_list:
            if haversine((r[2], r[3]), (data_l[i][2], data_l[i][3])) <= 3:
                temp += 1
        if temp == 0:
            result_list.append(data_l[i])
        if len(result_list) >= 5:
            break
    
    result = []
    count = 1
    for line in result_list:
        temp={}
        temp["id"] = count
        temp["lat"] = line[2]
        temp["lng"] = line[3]
        temp["area_name"] = regionName(line[2], line[3])
        count += 1
        result.append(temp)
    
    return result

'''
def searchTop10(data):
    search_keyword = ['병원', '은행', '동사무소']
    for i in data:
        url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?{}'.format("x={0}&y={1}".format(i[2],i[1]))
        headers = {"Authorization": "KakaoAK fc1a434c73667b0fe3707f6023b3cc81"}
        result = json.loads(str(requests.get(url, headers=headers).text))
        regal_area = result['documents'][1]['address_name']
        regal_region = result['documents'][1]['region_2depth_name']
        print("1")
        if env_col.find({"$text":{"$search": regal_region}}).count() == 0:
            print("2")
            for keyword in search_keyword:
                print("3")
                livecrawler.area_crawler(regal_area, keyword)
                print("4")
'''


address = '서울시 강남구 테헤란로 242'
brand = ["스타벅스", "맥도날드","GS25","올리브영","cu","세븐일레븐"]

print('회사 주소 :', address)
data = maslAreaSelector(address)
print('선택한 브랜드 :', brand)
start = time.time()
result = areaTop10(brand, data, address)
for i in range(5):
    print(f"결과{i+1} :", result[i]['area_name'])
print("areaTop10 걸린시간 :", time.time()-start)
print("전체 걸린시간 :", time.time() - check_time)