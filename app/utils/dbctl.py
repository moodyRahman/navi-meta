from pymongo import MongoClient


_client = MongoClient(
    'moody.wtf', 27017, 
    # username='finalproj', 
    # password='thluffy', # yes, we know it's bad practice
    authSource='sitedata'
)
# _client = MongoClient('localhost', 27017)
accounts = _client.sitedata.accounts # basic account information
userdata = _client.sitedata.userdata # user's essays, colleges, etc.
colleges = _client.sitedata.colleges # college information

def store(collection, contents):
    return collection.insert(contents)

def find(collection, criteria):
    return list(collection.find(criteria))