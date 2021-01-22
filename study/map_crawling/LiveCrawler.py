import json
import requests
import argparse

import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup

import pandas as pd

# 크롬 드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('headless') # 브라우저 창 안 뜨도록 프로그램 상에서만 크롤링 동작
options.add_argument('lang=ko_KR') # 언어는 한국어

# 크롬 드라이버 호출
driver_path = "tools/chromedriver.exe" # 다운로드 : https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(os.path.join(os.getcwd(), driver_path), options=options)

# 2개 브라우저 필요 (구글맵, 카카오맵)
driver.execute_script('window.open("about:blank", "_blank");')
driver.execute_script('window.open("about:blank", "_blank");')

tabs = driver.window_handles

sleep(3)
# 구글맵
driver.switch_to.window(tabs[0])
driver.get('https://www.google.co.kr/maps/@37.597491,126.9258391,14z')

sleep(3)

# 카카오맵
driver.switch_to.window(tabs[1])
driver.get('https://map.kakao.com/')

def area_crawler(top_lat, top_lng, btm_lat, btm_lng):
    # 크롬 드라이버는 전역 변수
    global driver

    # 빈 데이터프레임 생성 : https://shydev.tistory.com/29
    df = pd.DataFrame(columns=['fac_id', 'fac_type', 'fac_name', 'fac_addr', 'fac_geo_lat', 'fac_geo_lng'])
    # geo_list = [top_lat, top_lng, btm_lat, btm_lng]

    # 변수 선언 : 정사각형 영역 중심좌표 계산
    lat_center = (top_lat + btm_lat) / 2
    lng_center = (top_lng + btm_lng) / 2

    # 구글에 검색할 "위도값, 경도값"
    geo_keyword = str(lat_center) + ", " + str(lng_center)

    facility = ['병원', '공원', '은행']

    # 4초 대기
    driver.implicitly_wait(4)

    # 검색 함수 실행
    df_total = search(geo_keyword, facility, df)

    # 크롤링 후 .csv 로 변환
    df_total.to_csv("raw_data/facility_in_district.csv")

    # 웹드라이버 셧 다운
    driver.quit()
    print("크롤링 완료")

def search(keyword, facility, df):

    global driver

    sleep(4)
    driver.switch_to.window(tabs[0])

    df_total = pd.DataFrame(columns=['fac_id', 'fac_type', 'fac_name', 'fac_addr', 'fac_geo_lat', 'fac_geo_lng'])

    # xPath 로 검색창 태그 추출
    search_area = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    sleep(2)

    # 검색어 입력
    search_area.send_keys(keyword)
    sleep(2)

    # 검색 Enter
    driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').send_keys(Keys.ENTER)


    # 검색된 정보가 있는 경우에만 탐색
    sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    addr = soup.select('#pane > div > div.widget-pane-content.scrollable-y > div > div > div:nth-of-type(8) > div > div.section-info-line > span.section-info-text > span.widget-pane-link')[0].text
    addr_data = addr.split(" ")
    addr = " ".join(addr_data[1:3])

    df_temp = list_crawler(addr, facility, df)
    df_total = df_total.append(df_temp)

    driver.switch_to.window(tabs[0])
    sleep(3)
    return df_total

# 한 페이지 목록을 받아서 크롤링 하는 함수
def list_crawler(addr, facility, df):

    for f in facility:
        keyword = addr + " " + f

        driver.switch_to.window(tabs[1])
        sleep(3)
        # xPath 로 검색창 태그 추출
        search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')

        # 검색어 입력
        search_area.send_keys(keyword)

        # 검색 Enter
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
        sleep(1)

        next_button = driver.find_element_by_xpath('//*[@id="info.search.place.more"]')
        next_button_class = next_button.get_attribute('class')

        if next_button_class == "more":
            xPath_next_button = '//*[@id="info.search.place.more"]'
            driver.find_element_by_xpath(xPath_next_button).send_keys(Keys.ENTER)
        else:
            pass
        sleep(3)
        try:
            while True: # 페이지들 크롤링이 전부 끝날 때까지 계속 [다음] 버튼으로 넘어감

                for i in range(1, 6):

                    # 한 덩어리에는 5개의 페이지가 존재 (1페이지 to 5페이지 / 6페이지 to 10페이지 / .. etc.)
                    xPath_page = '//*[@id="info.search.page.no' + str(i) + '"]'
                    driver.find_element_by_xpath(xPath_page).send_keys(Keys.ENTER)
                    sleep(1)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    # 한 페이지에 검색된 시설 리스트
                    fac_lists = soup.select('.placelist > .PlaceItem')

                    # 광고에 따라서 index 조정 필요 - 광고칸은 목록에서 4번째마다 등장
                    for i, place in enumerate(fac_lists):
                        if i >= 3:
                            i += 1

                        # 시설 이름
                        fac_name = place.select('.head_item > .tit_name > .link_name')[0].text

                        # 시설 주소
                        fac_addr = place.select('.info_item > .addr > p')[0].text
                        addr_list = fac_addr.split(" ")
                        addr_list = addr_list[:4]
                        fac_addr = " ".join(addr_list)

                        # 시설 카테고리
                        fac_type = place.select('.head_item > span')[0].text

                        # 매장 위도 경도
                        fac_geo_lat, fac_geo_lng = getGeoCode(fac_addr)

                        print('시설명:', fac_name, '| 시설주소: ', fac_addr, '| 시설분류:', fac_type)
                        print('위도:', fac_geo_lat, '| 경도:', fac_geo_lng)
                        print('----------------------------------------------------------------------')

                        # 데이터프레임에 데이터 .append
                        df = df.append(pd.DataFrame([['-', fac_type, fac_name, fac_addr, fac_geo_lat, fac_geo_lng]], columns=['fac_id', 'fac_type', 'fac_name', 'fac_addr', 'fac_geo_lat', 'fac_geo_lng']))

                # [다음] 버튼의 클래스 속성 값이 next 이면 계속 넘어가고, 아니면(next disabled) 크롤링 종료
                next_button = driver.find_element_by_xpath('//*[@id="info.search.page.next"]')
                next_button_class = next_button.get_attribute('class')

                if next_button_class == "next":
                    xPath_next_button = '//*[@id="info.search.page.next"]'
                    driver.find_element_by_xpath(xPath_next_button).send_keys(Keys.ENTER)
                else:
                    break

        except ElementNotInteractableException as ni:
            print('No More Result', ni)

        except Exception as e:
            print("Error", e)

        finally:
            search_area.clear()

        # 웹드라이버 임시 종료 - 종료하면 세션 만료로 오류 발생해서 주석 처리
        # driver.close()
    return df

# KAKAO MAP API 연동하여 위도 경도 받아오는 함수
def getGeoCode(address):

    # 주소 정보 입력
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format(address)

    # KAKAO REST API 토큰 인증 - 2021/1/21 부터 2개월 유효
    headers = {"Authorization": "KakaoAK db80de33bb89c7f47c6cb2948ca14e90"}

    # url 로 위경도 정보 호출
    result = json.loads(str(requests.get(url, headers=headers).text))

    # 위경도 정보 호출 실패 시 위도 경도 값 각각 "-" 값으로 대체
    if result['documents'] == []:
        return "-", "-"
    else:
        match_first = result['documents'][0]['address']

        # y 좌표(위도), x 좌표(경도) 반환
        return float(match_first['y']), float(match_first['x'])
