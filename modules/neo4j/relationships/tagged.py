from re import T
from typing import List
from . import driver,Relationship

class Tagged(Relationship):
    @staticmethod
    def add(post:int,tag:int):
        if (type(post),type(tag)) != (int,int):
            raise TypeError(f"Post IDs not used, ({post},{tag})")
        with driver.session() as tx:
            tx.run("""
                MATCH (p:Post) WHERE ID(p) = $post
                MATCH (t:Tag) WHERE ID(t) = $tag
                CREATE (p)-[r:Tagged]->(t)
                SET r.time = timestamp()
                """,
                post=post,tag=tag)

    @staticmethod
    def bulk_add(postID:int,tagIDs:List[int]):
        with driver.session() as tx:
            tx.run("""
                MATCH (p:Post) WHERE ID(p) = $post
                MATCH (t:Tag) WHERE ID(t) IN $tagIDs
                CREATE (p)-[r:Tagged]->(t)
                SET r.time = timestamp()
                """,
                post=postID,tagIDs=tagIDs)

    
    @staticmethod
    def remove(postID:int,tagID:str):
        with driver.session() as tx:
            tx.run("""
                MATCH (p:Post) WHERE ID(p) = $post
                MATCH (t:Tag) WHERE ID(t) = $tag
                MATCH (p)-[r:Tagged]->(t)
                DELETE r
                """,
                post=postID,tag=tagID)