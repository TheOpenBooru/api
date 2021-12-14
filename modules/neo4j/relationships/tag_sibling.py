from . import Relationship,driver

class SiblingTag(Relationship):
    @staticmethod
    def add(sibling_1:int,sibling_2:int):
        with driver.session() as tx:
            tx.run("""
                MATCH (a:Tag) WHERE ID(a) = $s1
                MATCH (b:Tag) WHERE ID(b) = $s2
                CREATE (a)-[:TagSibling]->(b)
                """,
                s1=sibling_1,s2=sibling_2)
    
    @staticmethod
    def remove(sibling_1:int,sibling_2:int):
        with driver.session() as tx:
            tx.run("""
                MATCH (a:Tag) WHERE ID(a) = $s1
                MATCH (b:Tag) WHERE ID(b) = $s2
                MATCH (a)-[r:TagParent]-(b)
                DELETE r
                """,
                s1=sibling_1,s2=sibling_2)