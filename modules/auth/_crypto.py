from typing import Literal, Union
import os
import time
import jwt
import logging
from passlib.hash import argon2
from . import _database as db

SECRET = os.getenv('TOKEN_SECRET')

hashPassword = lambda password: argon2.using(rounds=4).hash(password)
verifyPassword = lambda password, hash: argon2.verify(password, hash)
isPasswordInvalid = lambda password: password == 'password'

def create(id:int,password:str):
    if db.get(id):
        raise KeyError("User ID already exists")
    if isPasswordInvalid(password):
        raise ValueError("Password Does Not Meet Requirements")
    
    hash = hashPassword(password)
    db.create(id,hash)

def login(id:int,password:str,data:dict) -> str:
    hash = db.get(id)
    if not hash:
        raise LookupError('Non-Existant User ID')
    if not verifyPassword(password,hash):
        return False
    try:
        token = jwt.encode(
            payload=data,
            key=SECRET,
            algorithm='HS256',
            headers={
                'exp':time.time() + (60*60*24*7)
            }
        )
    except Exception as e:
        fmtE = str(e).replace('\n','\\n')
        logging.debug(f'Login Failed with exception:{fmtE}')
        return False
    else:
        return token

def verify(token:str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
        data = jwt.decode(
            token,
            key=SECRET,
            algorithms=[header['alg']]
        )
    except Exception:
        return False
    else:
        return data


def changePassword(id:int,old_password:str,new_password:str):
    old_hash = db.get(id)
    if not old_hash:
        raise LookupError ('Non-Existant User ID')
    if isPasswordInvalid(new_password):
        raise ValueError("Password Does Not Meet Requirements")
    if not verifyPassword(old_password,old_hash):
        raise ValueError("Old Password isn't correct")
    else:
        newHash = hashPassword(new_password)
        db.set(id,newHash)
