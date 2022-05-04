from dataclasses import dataclass

@dataclass()
class User:
    username:str
    hash:str
    secret_2fa:str|None = None

users = {}

def create(user:User):
    users[user.username] = user

def update_hash(username:str,hash:str):
    users[username].hash = hash

def update_secret(username:str,secret:str):
    users[username].secret_2fa = secret

def get(username:str) -> User | None:
    return users.get(username,None)

def delete(username:str):
    users.pop(username,None)