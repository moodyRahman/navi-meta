import mongoengine


class Essay(mongoengine.Document):
    timestamp = mongoengine.DateTimeField()
    body = mongoengine.StringField()
    ispublic = mongoengine.BooleanField()


class User(mongoengine.Document):
    title = mongoengine.StringField()
    user = mongoengine.StringField()
    password = mongoengine.StringField()
    essays = mongoengine.ListField(Essay)

