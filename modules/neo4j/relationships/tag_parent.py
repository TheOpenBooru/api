from . import Relationship,driver

class ParentTag(Relationship):
    @staticmethod
    def add(child:str,parent:str):
        with driver.session() as tx:
            tx.run("""
                MATCH (c:Tag) WHERE ID(c) = $child
                MATCH (p:Tag) WHERE ID(p) = $parent
                CREATE (c)-[:TagParent]->(p)
                """,
                child=child,parent=parent)
    
    @staticmethod
    def remove(child:str,parent:str):
        with driver.session() as tx:
            tx.run("""
                MATCH (c:Tag) WHERE ID(c) = $child
                MATCH (p:Tag) WHERE ID(p) = $parent
                MATCH (c)-[r:TagParent]->(p)
                DELETE r
                """,
                child=child,parent=parent)