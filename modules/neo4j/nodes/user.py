from . import Node,driver,utils,measureTiming
import logging
from cachetools import TTLCache,cached


with driver.session() as tx:
    tx.run("CREATE INDEX user_indexes IF NOT EXISTS FOR (u:User) ON (u.created,u.name)")
    # tx.run("CREATE CONSTRAINT user_schema IF NOT EXISTS FOR (u:User) REQUIRE u.name IS UNIQUE")

class User(Node):
    @staticmethod
    @measureTiming
    def create(username:str) -> int:
        if utils.isUsernameUsed(username):
            raise KeyError
        with driver.session() as tx:
            data = tx.run("""
                        CREATE (u:User {
                            name:$name,
                            avatar_url:"",
                            description:"",
                            created:timestamp()
                        })
                        SET u.id = ID(u)
                        RETURN id(u)""",
                        name=username).value()
            
        return data[0]

    @staticmethod
    @cached(cache=TTLCache(maxsize=2048,ttl=3600))
    @measureTiming
    def get(*,id:int=None,name:str=None) -> dict:
        query = """
            OPTIONAL MATCH (u)-[:CreatedPost]->(p:Post)
            OPTIONAL MATCH (u)-[:View]->(h:Post)
            OPTIONAL MATCH (u)-[:Commented]->(c:Comment)
            RETURN
                u as user,
                collect(p) AS posts,
                collect(h) AS history,
                collect(c) AS comments
            """
        with driver.session() as tx:
            if id:
                response = tx.run(
                    "MATCH (u:User { id: $id })" + query,
                    id=id).data()
            elif name:
                response = tx.run(
                    "MATCH (u:User { name: $name })" + query,
                    name=name).data()
            else:
                raise ValueError(f"Must specify either id or name: {id=} {name=}")
        
        if not response:
            return None
        
        data = response[0]['user']
        data['posts'] = response[0]['posts']
        data['history'] = response[0]['history']
        data['comments'] = response[0]['comments']
        return data

    @measureTiming
    def delete(id:int=None) -> bool:
        with driver.session() as tx:
            tx.run("""
                MATCH (n:User {id:$id})
                DETACH DELETE n
                """,
                id=id)