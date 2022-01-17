import sqlite3

conn = sqlite3.connect('./data/passwords.sqlite3')
conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id      INT    PRIMARY KEY,
        hash    STRING,
        secret  STRING
    );""")


def create(id:int,hash:str):
    try:
        get(id)
    except KeyError:
        pass
    else:
        raise KeyError("User ID already exists")
    
    with conn:
        conn.execute(
            "INSERT INTO users VALUES(?,?,?)",
            (id,hash,None)
        )

def get(id:int) -> tuple[str,str]:
    with conn:
        cur = conn.execute(
            "SELECT hash,secret FROM users WHERE id=?",
            (id,)
        )
    data = cur.fetchone()
    if data:
        return data
    else:
        raise KeyError("User with that ID doesn't exist")

def set_hash(id:int,hash:str):
    with conn:
        conn.execute(
            "UPDATE users SET hash=? WHERE id=?",
            (hash,id)
        )

def set_2fa(id:int,secret:str):
    with conn:
        conn.execute(
            "UPDATE users SET secret=? WHERE id=?",
            (secret,id)
        )

def delete(id:int) -> None:
    with conn:
        conn.execute(
            "DELETE FROM users WHERE id = ?",
            (id,)
        )

def clear() -> None:
    with conn:
        conn.execute("DELETE FROM users")