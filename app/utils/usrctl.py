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


def create_user(name, password, mode='user'):
    '''
    Attempts to create a user with given username and password. 

    Raises ValueError if invalid.
    '''

    if match(name_form, name):
        dupes = dbctl.User.objects(name=name)
        if len(dupes):
            raise ValueError(f'Username "{name}" already exists')
        newuser = dbctl.User(name=name, password=password, accounttype=mode)
        newuser.save()
    else:
        raise ValueError('Username must be 3 to 20 alphnumeric characters or underscores')

def add_college_to_user(username, college_name):
    '''
    Adds college object to user

    Uses user and college names
    '''
    
    user = dbctl.find_user(username)
    if not user:
        raise ValueError(f'User "{username}" does not exist')

    college = dbctl.find_user(college_name)
    if not college:
        raise ValueError(f'College "{college_name}" does not exist')

    college = dbctl.from_allcollege(college)

    # code to update user's Colleges list