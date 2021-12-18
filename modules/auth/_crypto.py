import os
import time
import jwt
import logging
from passlib.hash import argon2

from . import AuthError, BadTokenError,_database as db

hashPassword = lambda password: argon2.using(rounds=4).hash(password)
verifyPassword = lambda password, hash: argon2.verify(password, hash)
isPasswordInvalid = lambda password: password == 'password' or len(password) < 8

def create(id:int,password:str):
    if db.get(id):
        raise KeyError("User ID already exists")
    if isPasswordInvalid(password):
        raise ValueError("Password Does Not Meet Requirements")
    
    hash = hashPassword(password)
    db.create(id,hash)

def login(id:int,password:str,*,data:dict={},expiration:int=6604800) -> str:
    hash = db.get(id)
    if not hash:
        raise KeyError('Non-Existant User ID')
    elif not isinstance(data,dict):
        raise TypeError("Payload is not a dict")
    elif not verifyPassword(password,hash):
        raise AuthError("Invalid Password or Username")
    
    payload = {
        "user":id,
        "data":data,
        "exp" :time.time() + expiration
        }
    token = jwt.encode(payload,os.getenv('JWT_SECRET'))
    return token

def decode(token:str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
        data = jwt.decode(
            token,
            key=os.getenv('JWT_SECRET'),
            algorithms=[header['alg']]
        )
    except Exception:
        raise BadTokenError("Token was Invalid")
    if not db.get(data['user']):
        raise KeyError("User has been deleted")
    else:
        return data


def update(id:int,old_password:str,new_password:str):
    old_hash = db.get(id)
    if not old_hash:
        raise KeyError('Non-Existant User ID')
    elif isPasswordInvalid(new_password):
        raise ValueError("Password Does Not Meet Requirements")
    elif not verifyPassword(old_password,old_hash):
        raise AuthError("Old Password is Incorrect")
    else:
        newHash = hashPassword(new_password)
        db.set(id,newHash)
