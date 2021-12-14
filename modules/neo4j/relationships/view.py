from . import driver,Relationship

class View(Relationship):
    @staticmethod
    def add(user:int,post:int,duration:int):
        with driver.session() as tx:
            tx.run("""
                MATCH (u:User {id:$uID})
                MATCH (p:Post {id:$pID})
                CREATE (u)-[:Viewed {time:timestamp(),duration:$dur}]->(p)
                """,uID=user,pID=post,dur=duration)
    
    def get(user:int=None,post:int=None):
        
        with driver.session() as tx:
            tx.run("""
                MATCH (u:User)
                   """)