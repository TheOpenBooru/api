from . import driver,Node,measureTiming
import logging
from cachetools import TTLCache,cached

with driver.session() as tx:
    tx.run("CREATE INDEX tag IF NOT EXISTS FOR (t:Tag) ON (t.created,t.name)")

class Tag(Node):
    TYPES = {"generic","author","character","series","genre","meta"}

    @staticmethod
    @measureTiming
    def create(name:str,type:str='generic') -> int:
        if Tag.get(name=name):
            raise KeyError("Attempted to create duplicate tag")
        if type not in Tag.TYPES:
            raise ValueError("Attempted to create invalid tag type")
        
        with driver.session() as tx:
            data = tx.run("""
                        CREATE (t:Tag {
                                name: $name,
                                type: $type,
                                created: timestamp()
                            })
                        SET t.id = ID(t)
                        RETURN ID(t)""",
                        name=name,type=type).value()[0]
            
        return data

    @staticmethod
    @cached(cache=TTLCache(maxsize=2048,ttl=3600))
    @measureTiming
    def get(*,id:int=None,name:str=None) -> dict:
        query = """
            OPTIONAL MATCH (posts:Post)-[:Tagged]->(t)
            OPTIONAL MATCH (t:Tag)-[:TagParent]->(parent:Tag)
            OPTIONAL MATCH (t:Tag)-[:TagSibling]->(sibling:Tag)
            RETURN  t as tag,
                    COLLECT(sibling) as siblings,
                    COLLECT(parent) as parents,
                    COUNT(posts) as count
            """
        with driver.session() as tx:
            if id:
                response = tx.run(
                    "MATCH (t:Tag { id:$id })" + query,
                    id=id).data()
            elif name:
                response = tx.run(
                    "MATCH (t:Tag { name:$name })" + query,
                    name=name).data()
            else:
                raise ValueError(f"Must specify either id or name: {id=} {name=}")
        
        if not response:
            return None

        data = response[0]['tag']
        data['aliases'] = response[0]['siblings']
        data['parent'] = response[0]['parents']
        data['count'] = response[0]['count']
        
        return data

    @staticmethod
    @cached(cache=TTLCache(1,60*60*12))
    @measureTiming
    def list() -> list:
        with driver.session() as tx:
            data = tx.run("""
                MATCH (t:Tag)
                RETURN t.name as name
                """).data()
        
        tags = []
        for row in data:
            tag = row['name']
            tags.append(tag)
        
        return tags