import pymongo

conn = pymongo.MongoClient()

masl = conn.masl
masl_structure = masl.structure
masl_type = masl.type

masl_structure.insert_many(
    [
        {
            "sotre_id":"congs000001",
            "type":"convenient store",
            "brand":"gs25",
            "store_name":"서울대점",
            "store_address":"서울시 관악구 대학로 00-000",
            "geo_lat":"lat",
            "geo_lng":"lng"
        },
        {
            "sotre_id":"retol000001",
            "type":"retail",
            "brand":"olive young",
            "store_name":"서울역점",
            "store_address":"서울시 용산구 남대문로 000-0000",
            "geo_lat":"lat",
            "geo_lng":"lng"
        }
    ]
)

masl_type.insert_many(
    [
        {"type":"convenient store", "brand":"gs25/cu/세븐일레븐 등"},
        {"type":"cafe", "brand":"스타벅스/투썸플레이스/폴바셋 등"},
        {"type":"retail", "brand":"올리브영/라라블라 등 소매점"},
        {"type":"mart", "brand":"이마트/이마트 에브리데이/홈플러스 등 (SSM 포함)"},
        {"type":"bus stop", "brand":"버스정류장 (마을버스 포함)"},
        {"type":"metro", "brand":"지하철역"},
        {"type":"fastfood", "brand":"맥도날드/서브웨이/버거킹 등 패스트푸드"}
    ]
)

docs = masl_structure.find()
for doc in docs:
    print(doc)

docs = masl_type.find()
for doc in docs:
    print(doc)

