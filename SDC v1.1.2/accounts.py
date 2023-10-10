import hashlib

import database



def checkLoginDataFormat(user):
    if user.strip().isalnum() is True and len(user.strip()) <= 15:
        return True
    else:
        return False

def login(user):
    if checkLoginDataFormat(user.strip()) is True:
        return database.hasAccount(user.strip())
    else:
        return False

def createAccount(user):
    if checkLoginDataFormat(user.strip()) is True:
        if database.hasAccount(user.strip()) is False:
            return database.addAccount(user.strip())

    return False