import mongoengine as mgng
from mongoengine import connect
from datetime import datetime

connect('sitedata', host="moody.wtf", port=27017)

class MetaData(mgng.EmbeddedDocument):
    '''MetaData class for MongoEngine
        Embedded document for Essays and AllColleges
    Consists of
        mu_sentence_length: Mean sentence length, in words
        sentence_count: Amount of sentences, in words
        mu_word_length: Mean word length, in characters
        word_count: Word count
        word_frequencies: Dictionary of {word:frequency}, excludes trivial words (to be decided)
    '''
    mu_sentence_length = mgng.FloatField()
    sentence_count = mgng.IntField()
    mu_word_length = mgng.FloatField()
    word_count = mgng.IntField()
    word_frequencies = mgng.DictField()

class Essay(mgng.EmbeddedDocument):
    '''Essay class for MongoEngine
        Embedded document for User embedded Colleges

    Consists of 
        timestamp: Last edited time 
        body: User's essay
        question: Essay prompt
        meta: Metadata (MetaData document)
    '''
    timestamp = mgng.DateTimeField()
    body = mgng.StringField()
    prompt = mgng.StringField()
    ispublic = mgng.BooleanField()
    meta = mgng.EmbeddedDocumentField(MetaData)

class College(mgng.EmbeddedDocument):
    '''College class for MongoEngine
        Embedded document for Users

    Consists of 
        name: College name
        status: Acceptance status ('Accepted', 'Waitlisted', 'Rejected', 'No result')
        rank: User choice rank
        essays: User's essays
    '''
    name = mgng.StringField()
    status = mgng.StringField()
    rank = mgng.IntField()
    essays = mgng.ListField(mgng.EmbeddedDocumentField(Essay))

def from_allcollege(allcollege, rank=-1):
    '''Converts AllCollege instance to User embedded College'''
    return dbctl.College(
        name = allcollege.name,
        status = 'No result',
        rank = rank,
        essays = [
            Essay(
                timestamp = datetime.now(),
                prompt = prompt,
                ispublic = False
            )
            for prompt, word_count in allcollege.prompts
        ],
    )



class User(mgng.Document):
    '''User class for MongoEngine
    
    Consists of
        name: Username
        password: Password (not hashed while in development)
        colleges: List of colleges the user is writing essays for
        accounttype: 'user' or 'admin'
    '''

    name = mgng.StringField(required=True)
    password = mgng.StringField(required=True)
    colleges = mgng.SortedListField(mgng.EmbeddedDocumentField(College), ordering="rank")
    accounttype = mgng.StringField(required=True)

def find_user(name):
    '''Finds user instance based on name
    
    Returns False if no user is found'''
    results = dbctl.User.objects(name = name)
    if len(results):
        return results[0]
    return False

class AllCollege(mgng.Document):
    '''College class for MongoEngine
        Used for storage of college statistics

    Consists of 
        prompts: essay prompt
        meta: metadata (MetaData document) about all essays
    '''

    name = mgng.StringField()
    prompts = mgng.DictField() # {prompt:word_count}
    meta = mgng.EmbeddedDocumentField(MetaData)
    accepted = mgng.IntField()
    rejected = mgng.IntField()

def find_college(name):
    '''Finds college instance based on name
    
    Returns False if no college is found'''
    results = dbctl.AllCollege.objects(name = name)
    if len(results):
        return results[0]
    return False