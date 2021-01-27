from flask import Flask, render_template, request, url_for, redirect
from masldb import MaslDataInput
from crawler import storeCrawler
import maslAreaSelector

app = Flask(__name__)

@app.route('/')
def init_page():
    return render_template('init.html')

@app.route('/UserInfo')
def UserInfo():
    return(render_template('UserInfo.html'))

@app.route('/UserInfo/salary', methods=['GET', 'POST'])
def salary():
    if request.method == 'GET':
        return render_template('salary.html')
    if request.method == 'POST':
        address = request.form['address']
        store_list = request.form.getlist('cafe')
        home = crawler.getGeoCode(address)
        stations = maslAreaSelector.NearMetro(home)
        lines = maslAreaSelector.getMetroLine(stations)
        metro_area_list = maslAreaSelector.allMetroLineStations(lines)
        bus_stations = maslAreaSelector.nearBusStop(home)

        return render_template('home.html')



if __name__ == '__main__':
    app.run(debug = True)