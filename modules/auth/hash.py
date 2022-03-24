from passlib.hash import argon2

def hash(password:str):
    return argon2.hash(password)

def compare(password:str,hash:str):
    return argon2.verify(password,hash)
