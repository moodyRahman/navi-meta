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


class College(mgng.EmbeddedDocument):
    name = mgng.StringField()
    status = mgng.StringField()
    rank = mgng.IntField()
    essays = mgng.ListField(mgng.EmbeddedDocumentField(Essay))


class User(mgng.Document):
    """Defines what a user consists of
    Timestamp, body, and ispublic


class User(mongoengine.Document):
    title = mongoengine.StringField()
    user = mongoengine.StringField()
    password = mongoengine.StringField()
    essays = mongoengine.ListField(Essay)

