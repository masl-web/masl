from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# 초기 접속 페이지
@app.route('/')
def init_page():
    return render_template('init.html')

# 유정 유형 선택 페이지(직장인) 추후 학생 기타 추가 예정
@app.route('/UserInfo')
def UserInfo():
    return(render_template('UserInfo.html'))

# 유저 정보 입력 페이지
@app.route('/UserInfo/salary', methods=['GET', 'POST'])
def salary():
    if request.method == 'GET':
        return render_template('salary.html')
    if request.method == 'POST':
        address = request.form['address'] # 직장 주소
        store_list = request.form.getlist('cafe') # 매장 선택 정보
        # home 변수에 직장 주소 geocode 변환 값 저장
        home = maslAreaSelector.getGeoCode(address)
        # stations 변수에 직장 주소 반경 500m 내 지하철 역 리스트 저장
        stations = maslAreaSelector.NearMetro(home)
        # lines 해당 지하철 역을 지나는 지하철 호선 리스트 저장
        lines = maslAreaSelector.getMetroLine(stations)
        # metro_area_list = 지하철 호선 내 모든 역 리스트 저장
        metro_area_list = maslAreaSelector.allMetroLineStations(lines)
        # bus_stations 변수에 home에서 100m이내 모든 버스 정류장 리스트 저장
        bus_stations = maslAreaSelector.nearBusStop(home)
        
        return render_template('home.html')



if __name__ == '__main__':
    app.run(debug = True)
