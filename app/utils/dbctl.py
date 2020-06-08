from pymongo import MongoClient


_client = MongoClient(
    'moody.wtf', 27017, 
    # username='finalproj', 
    # password='thluffy', # yes, we know it's bad practice
    authSource='sitedata'
)
# _client = MongoClient('localhost', 27017)
users = _client.sitedata.users
colleges = _client.sitedata.colleges

def store(collection, contents):
    return collection.insert(contents)

def find(collection, criteria):
    return list(collection.find(criteria))