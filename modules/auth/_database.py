import sqlite3

conn = sqlite3.connect('./data/passwords.sqlite3')
conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id   INT    PRIMARY KEY,
        hash STRING
    );""")


def create(id:int,hash:str) -> None:
    if get(id):
        raise KeyError("Duplicate ID Creation")
    else:
        with conn:
            conn.execute(
                "INSERT INTO users VALUES(?,?)",
                (id,hash)
            )

def get(id:int) -> str:
    with conn:
        cur = conn.execute(
            "SELECT hash FROM users WHERE id=?",
            (id,)
        )
    data = cur.fetchone()
    if data:
        return data[0]
    else:
        return ""

def set(id:int,hash:str) -> None:
    with conn:
        conn.execute(
            "UPDATE users SET hash=? WHERE id=?",
            (hash,id)
        )

def delete(id:int) -> None:
    with conn:
        conn.execute(
            "DELETE FROM users WHERE id = ?",
            (id,)
        )