import json
import requests
import pymongo
from haversine import haversine
from crawler import getGeoCode

class maslAreaSelector:
    def __init__(self):
        masl_client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = masl_client['LocationData']
        store_col = db['StoreData']
        metro_col = db['MetroData']
        bus_stop_col = db['BusStopData']


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
        data = []
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
            data.append(allStationInfo)
        return data

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


if __name__ = "__main__":
    main()