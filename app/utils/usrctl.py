from re import match
from ..utils import dbctl

name_form = '\w{3,20}'


def login(name, password):
    '''
    Check name and password against database contents

    If successful, returns a dictionary containing user information.

    Otherwise returns `False`.
    '''

    user = dbctl.User.objects(name=name)
    if not user or user[0]['password'] != password:
        return False
    else:
        return user[0]


def create(name, password, mode='user'):
    '''
    Attempts to create a user with given username and password. 

    Raises ValueError if invalid.
    '''

    if match(name_form, name):
        dupes = dbctl.User.objects(name=name)
        if dupes:
            raise ValueError('Username already exists')
        newuser = dbctl.User(name=name, password=password, accounttype=mode)
        newuser.save()
    else:
        raise ValueError('Username must be 3 to 20 alphnumeric characters or underscores')
