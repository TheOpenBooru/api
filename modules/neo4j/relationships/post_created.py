from . import Relationship,driver

class CreatedPost(Relationship):
    @staticmethod
    def add(user:int,post:int):
        if (type(user),type(post)) != (int,int):
            raise TypeError(f"Post IDs not used, ({user},{post})")
        with driver.session() as tx:
            tx.run("""
                MATCH (u:User) WHERE ID(u) = $uID
                MATCH (p:Post) WHERE ID(p) = $pID
                CREATE (u)-[:CreatedPost]->(p)
                """,
                uID=user,pID=post)
