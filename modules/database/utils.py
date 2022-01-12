import os
from . import _driver

def _db_run(query,**kwargs):
    with _driver.session() as session:
        return session.write_transaction(
            lambda tx: tx.run(query,**kwargs).data()
        )

def clear():
    "Clears the database, requires env DEPLOYMENT set to 'TESTING'"
    if os.getenv("DEPLOYMENT") == "TESTING":
        _db_run("MATCH (n) DETACH DELETE n")
    else:
        raise Exception("Attempted to clear database in production")

class isUnique:
    @staticmethod
    def user_name(name:str) -> bool:
        result = _db_run(
                "MATCH (n:User {name:$name}) RETURN n",
                name=name
            )
        return not bool(result)

    @staticmethod
    def user_email(email:str) -> bool:
        result = _db_run(
                "MATCH (n:User {email:$email}) RETURN n",
                email=email
            )
        return not bool(result)

    @staticmethod
    def image_md5(md5:str) -> bool:
        result = _db_run(
                "MATCH (n:Image {md5:$hash}) RETURN n",
                hash=md5
            )
        return not bool(result)
    
    @staticmethod
    def image_url(url:str) -> bool:
        result = _db_run(
                "MATCH (n:Image {url:$url}) RETURN n",
                url=url
            )
        return not bool(result)