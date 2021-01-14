## crawler.py

카카오맵을 크롤링하여 **매장 정보 csv 데이터**를 생성하는 파일입니다. 

### Prerequisites

아래 사항들이 설치가 되어있어야합니다.

```
pip install requests argparse selenium beautifulsoup4 pandas
```

## Running

Command-Line Arguments 를 필요에 따라 지정하여 실행합니다.

```
python crawler.py --city "서울시" --store "스타벅스" --output_file "starbucks_seoul(geo).csv"
```

### Details

| Function | Description |
| --- | --- |
| search() | 매장을 검색하는 함수 |
| crawling() | 검색된 매장을 크롤링하는 함수 |
| getGeoCode() | 카카오맵 API를 호출하여 해당 주소의 Geocode(위도, 경도)를 반환하는 함수 |
