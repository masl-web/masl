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

def main():
    # 크롬 드라이버는 전역 변수
    global driver

    # 외부 변수 할당
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', type=str, help="set city", default='서울시')
    parser.add_argument('--store', type=str, help="set store", default='스타벅스')
    parser.add_argument('--output_file', type=str, help="set output filename", default='starbucks_seoul(geo).csv')

    args = parser.parse_args()

    city = args.city
    store = args.store
    output_csv_name = args.output_file

    # 빈 데이터프레임 생성 : https://shydev.tistory.com/29
    df = pd.DataFrame(columns=['store_id', 'store_type', 'store_brand', 'store_name', 'store_addr', 'store_geo_lat', 'store_geo_lng'])

    # 변수 선언 : 크롤링하고자 하는 매장에 따라 변경 가능
    keyword = city + " " + store

    # 4초 대기
    driver.implicitly_wait(4)

    # 카카오맵 메인 URL
    driver.get('https://map.kakao.com/')

    # 검색 및 크롤링 함수 실행
    df_total = search(keyword, store, df)

    print(df_total)

    # 크롤링 후 .csv 로 변환
    df_total.to_csv("raw_data/"+output_csv_name)

    # 웹드라이버 셧 다운
    driver.quit()
    print("크롤링 완료")

def search(keyword, store, df):
    global driver

    df_total = pd.DataFrame(columns=['store_id', 'store_type', 'store_brand', 'store_name', 'store_addr', 'store_geo_lat', 'store_geo_lng'])

    # xPath 로 검색창 태그 추출
    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')

    # 검색어 입력
    search_area.send_keys(keyword)

    # 검색 Enter
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
    sleep(1)

    # 검색된 정보가 있는 경우에만 탐색
    try:
        driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
        sleep(3)

        while True: # 페이지들 크롤링이 전부 끝날 때까지 계속 [다음] 버튼으로 넘어감

            for i in range(1, 6):

                # 한 덩어리에는 5개의 페이지가 존재 (1페이지 to 5페이지 / 6페이지 to 10페이지 / .. etc.)
                xPath_page = '//*[@id="info.search.page.no' + str(i) + '"]'
                driver.find_element_by_xpath(xPath_page).send_keys(Keys.ENTER)
                sleep(1)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 한 페이지에 검색된 매장 리스트
                store_lists = soup.select('.placelist > .PlaceItem')

                # 한 페이지 크롤링한 결과를 기존 데이터프레임에 .append
                df_temp = crawling(store_lists, store, df)
                df_total = df_total.append(df_temp)

            # [다음] 버튼의 클래스 속성 값이 next 이면 계속 넘어가고, 아니면(next disabled) 크롤링 종료
            next_button = driver.find_element_by_xpath('//*[@id="info.search.page.next"]')
            next_button_class = next_button.get_attribute('class')

            if next_button_class == "next":
                xPath_next_button = '//*[@id="info.search.page.next"]'
                driver.find_element_by_xpath(xPath_next_button).send_keys(Keys.ENTER)
            else:
                break

    except ElementNotInteractableException:
        print('No More Result')

    finally:
        search_area.clear()

    return df_total

# 한 페이지 목록을 받아서 크롤링 하는 함수
def crawling(store_lists, store, df):

    # 광고에 따라서 index 조정 필요 - 광고칸은 목록에서 4번째마다 등장
    for i, place in enumerate(store_lists):
        if i >= 3:
            i += 1

        # 매장 이름
        store_name = place.select('.head_item > .tit_name > .link_name')[0].text

        # 매장 주소
        store_addr = place.select('.info_item > .addr > p')[0].text

        # 매장 카테고리
        store_type = place.select('.head_item > span')[0].text

        # 매장 위도 경도
        store_geo_lat, store_geo_lng = getGeoCode(store_addr)

        print('매장명:', store_name, '| 매장주소: ', store_addr,'| 매장분류:', store_type)
        print('위도:', store_geo_lat, '| 경도:', store_geo_lng)
        print('----------------------------------------------------------------------')

        # 데이터프레임에 데이터 .append
        df = df.append(pd.DataFrame([['-', store_type, store, store_name, store_addr, store_geo_lat, store_geo_lng]], columns=['store_id', 'store_type', 'store_brand', 'store_name', 'store_addr','store_geo_lat','store_geo_lng']))

    return df
        # 웹드라이버 임시 종료 - 종료하면 세션 만료로 오류 발생해서 주석 처리
        # driver.close()

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

if __name__ == "__main__":
    main()