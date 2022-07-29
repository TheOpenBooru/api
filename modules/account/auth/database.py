from dataclasses import dataclass
import sqlite3
from typing import Union


@dataclass()
class User:
    username:str
    hash:str
    secret_2fa:Union[str,None] = None


conn = sqlite3.connect('./data/auth.db')
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hash TEXT,
        secret_2fa TEXT
    );
""")

def create(user:User):
    with conn:
        conn.execute(
            "INSERT INTO users (username,hash,secret_2fa) VALUES (?,?,?);",
            (user.username,user.hash,user.secret_2fa)
        )


def update_hash(username:str,hash:str):
    with conn:
        conn.execute(
            "UPDATE users SET hash=? WHERE username=?;",
            (hash,username)
        )


def update_secret(username:str,secret:str):
    with conn:
        conn.execute(
            "UPDATE users SET secret_2fa=? WHERE username=?;",
            (secret,username)
        )


def get(username:str) -> Union[User,None]:
    with conn:
        cursor = conn.execute(
            "SELECT hash,secret_2fa FROM users WHERE username=?;",
            (username,)
        )
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        hash,secret = data
        return User(
            username=username,
            hash=hash,
            secret_2fa=secret
        )


def delete(username:str):
    with conn:
        conn.execute(
            "DELETE FROM users WHERE username=?;",
            (username,)
        )


def clear():
    with conn:
        conn.execute("DELETE FROM users;")
