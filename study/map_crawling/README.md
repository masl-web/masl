## 개요

```crawler.py```는 카카오맵을 크롤링하여 **매장 정보 csv 데이터**를 생성하는 프로그램입니다.
1. Selenium 과 BeautifulSoup 으로 매장 정보 추출
2. 카카오맵 API 로 매장 주소를 사용하여 위성좌표 추출
3. 지정한 테이블 형식으로 데이터 적재

| 함수명 | 기능 |
| --- | --- |
| search() | 매장을 검색하는 함수 |
| crawling() | 검색된 매장을 크롤링하는 함수 |
| getGeoCode() | 카카오맵 API를 호출하여 해당 주소의 Geocode(위도, 경도)를 반환하는 함수 |


## 사전 조건

구동하려는 환경에서 아래 패키지의 설치가 필요합니다.

```
pip install requests argparse selenium beautifulsoup4 pandas
```

## 구동 방법

명령행 인자(Command-line arguments)를 필요에 따라 지정하여 실행합니다.

```
python crawler.py --city "서울시" --store "스타벅스" --output_file "starbucks_seoul(geo).csv"
```

## 이슈
* 카카오맵 API 가 변환하지 못하는 매장 주소 존재
  * [Google Geocode By Awesome Table](https://workspace.google.com/marketplace/app/geocode_by_awesome_table/904124517349) 사용하여 결측값 보완

