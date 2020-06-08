from utils import dbctl
from re import match

name_form = '\w{3,20}'

def login(name, password):
    '''
    Checks name and password against database contents

    If successful, returns a dictionary containing user information.

    Otherwise returns `False`.
    '''

    user = dbctl.find(dbctl.users, {'name':name})
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
        dupes = dbctl.find(dbctl.users, {'name':name})
        if dupes:
            raise ValueError('Username already exists')
        uid = dbctl.store(
            dbctl.users, 
            {'name':name, 'password':password, 'mode':mode}
        )
    else:
        raise ValueError('Username must be from 3 to 20 characters long, consisting only of alphanumeric characters and underscores')

