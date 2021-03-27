import csv
import pandas as pd
from app import db
from app import BusLine, BusStop
from app import app
import json
import requests

app.app_context().push()

def regionName(lat, lng):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?{}'.format("x={0}&y={1}".format(lng, lat))
    headers = {"Authorization": "KakaoAK 6f3c5c2ae909068ed7155b2e79237b82"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    regal_region = result['documents'][1]['region_2depth_name']
    return regal_region


# 버스라인 CSV 데이터 적재
# with open('./BackData/bus_line_seoul_final.csv') as file:
#     bus_line = pd.read_csv(file)
#     for i in range(0,39363):
#         record = BusLine(
#             bus_line = str(bus_line.loc[i][1]),
#             station_id = int(bus_line.loc[i][4])
#         )
#         db.session.add(record)
#     db.session.commit()

# 버스스탑 CSV 데이터 적재
bus_stop = pd.read_csv('BackData/bus_stop_seoul_final.csv', encoding='cp949')
bus_lines = pd.read_csv('BackData/bus_line_seoul_final.csv', encoding='utf-8')

for i in range(0,11179):
    temp_list= bus_lines[bus_lines["정류소ID"] == (int(bus_stop.loc[i][2]))]["노선명"].values.tolist()
    record = BusStop(
        station_name = bus_stop.loc[i][1],
        station_id = int(bus_stop.loc[i][2]),
        geo_lat = int(bus_stop.loc[i][4]),
        geo_lng = int(bus_stop.loc[i][5]),
        region_name = regionName(bus_stop.loc[i][4], bus_stop.loc[i][5]),
        bus_line = temp_list # 문제!! RDB로 가려면 이건 포기해야할것 같음. 또는 똑같은 걸 버스라인마다 나눠야함. 
    )
    db.session.add(record)
db.session.commit()
   
