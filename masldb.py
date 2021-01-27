import pymongo
import pandas as pd
from haversine import haversine

masl_client = pymongo.MongoClient('mongodb://localhost:27017/')

db = masl_client['LocationData']
store_col = db['StoreData']
metro_col = db['MetroData']
bus_stop_col = db['BusStopData']

metro = pd.read_csv('BackData/metro_station_seoul_final.csv', encoding='UTF-8')
for i in range(0,443):
    if " " not in metro.loc[i][1]:
        pass
    else:
        metro_col.insert({"type": "Metro", "line": metro.loc[i][1].split(" ")[1],
                        "station_name": metro.loc[i][1].split(" ")[0], "station_address": metro.loc[i][2],
                        "geo_lat": metro.loc[i][3], "geo_lng": metro.loc[i][4]})

bus_stop = pd.read_csv('BackData/bus_stop_seoul_final.csv', encoding='UTF-8')
for i in range(0,11178):
    bus_stop_col.insert({"type": "BusStop", "station_name": bus_stop.loc[i][1], "station_id": str(bus_stop.loc[i][3]), 
                    "geo_lat": bus_stop.loc[i][4], "geo_lng": bus_stop.loc[i][5]})

store = pd.read_csv('BackData/starbucks_seoul(geo)_final.csv', encoding='UTF-8')
for i in range(0,499):
    store_col.insert({"type": "Cafe", "brand": "starbucks", "store_name": store.loc[i][4], "store_address": store.loc[i][5],
                    "geo_lat": store.loc[i][6], "geo_lng": store.loc[i][7]})

def addStoreData(store_type, brand, store_name, store_address, geo_lat, geo_lng):
    query = {"$and": [{"store_name": self.str_name}, {"store_address": self.str_addr}]}
    if store_col.find(query) == None:
        store_col.insert({"type": store_type,
                        "brand": brand,
                        "store_name": store_name,
                        "store_address": store_address,
                        "geo_lat": geo_lat,
                        "geo_lng": geo_lng})

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
