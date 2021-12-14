from . import driver
import random

def isUsernameUsed(username) -> bool:
    with driver.session() as tx:
        result = tx.run(
            "MATCH (n:User {name:$username}) RETURN n",
            username=username
            ).value()
    return bool(result)

def isMD5Used(hash:str) -> bool:
    with driver.session() as tx:
        data = tx.run(
            "MATCH (n:Post {md5:$hash}) RETURN n",
            hash=hash).value()
    return bool(data)

def createTagSibling():
    ...
