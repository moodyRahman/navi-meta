import mongoengine as mgng
from mongoengine import connect

connect('sitedata', host="moody.wtf", port=27017)

class Essay(mgng.EmbeddedDocument):
    timestamp = mgng.DateTimeField()
    body = mgng.StringField()
    question = mgng.StringField()
    
#     wordfrequency = mgng.DictField()  # {String letter: int occurence}  # to be calculated when essay loaded, not in DB

#     meansentencelength = mgng.FloatField()
#     wordcount = mgng.IntField()
#     maxwordcount = mgng.IntField()
#     metapercentile = mgng.IntField()
#     ^^ some of the expected values ^^
    essaystats = mgng.DictField()


    ispublic = mgng.BooleanField()




class Essay(mongoengine.Document):
    timestamp = mongoengine.DateTimeField()
    body = mongoengine.StringField()
    ispublic = mongoengine.BooleanField()


class User(mongoengine.Document):
    title = mongoengine.StringField()
    user = mongoengine.StringField()
    password = mongoengine.StringField()
    essays = mongoengine.ListField(Essay)

