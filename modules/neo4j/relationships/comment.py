from . import Relationship,driver

class Commented(Relationship):
    @staticmethod
    def add(user:int,post:int,text:int):
        with driver.session() as tx:
            tx.run("""
                MATCH (u:User) WHERE ID(u) = $uID
                MATCH (p:Post) WHERE ID(p) = $pID
                CREATE (u)-[c:Comment]->(p)
                SET c.message = $msg
                SET c.created = timestamp()
                """,uID=user,pID=post,msg=text)

    def delete(id:int):
        with driver.session() as tx:
            tx.run("""
                MATCH (:User)-[c:Comment]->(:Post)
                WHERE ID(c) = $id
                DETACH c
                """,id=id)
