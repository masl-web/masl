import pymongo

mongo_host ='localhost'
connection = pymongo.MongoClient('mongodb://%s' % (mongo_host))

def conn_mongodb():
    try:
        connection.admin.command('ismaster')
        masl_structure = connection.masl.structure
    except:
        connection = pymongo.MongoClient('mongodb://%s' % (mongo_host))
        masl_structure = connection.masl.structure
    return blog_ab


