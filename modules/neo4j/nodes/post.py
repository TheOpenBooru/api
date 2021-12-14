from . import Node,utils,driver,measureTiming
import logging
from cachetools import TTLCache,cached

with driver.session() as tx:
    tx.run("CREATE INDEX post IF NOT EXISTS FOR (p:Post) ON (p.id,p.md5,p.created)")

class Post(Node):
    @staticmethod
    @measureTiming
    def create(hash:str,*,src:str="") -> int:
        if utils.isMD5Used(hash):
            raise KeyError
        
        with driver.session() as tx:
            data = tx.run("""
                        CREATE (p:Post {
                                md5:$hash,
                                source:$src,
                                created:timestamp()
                            })
                        set p.id = ID(p)
                        RETURN ID(p)
                        """,
                        src=src,hash=hash).value()
        return data[0]


    @staticmethod
    @measureTiming
    @cached(cache=TTLCache(maxsize=2048,ttl=3600))
    def get(*,id:int=None,md5:str=None) -> dict:
        query = """
                    OPTIONAL MATCH (p)-[:Tagged]->(t:Tag)
                    OPTIONAL MATCH (p)<-[:CreatedPost]-(u:User)
                    OPTIONAL MATCH (p)<-[c:Comment]-(:User)
                    OPTIONAL MATCH (p)<-[v:View]-(:User)
                    OPTIONAL MATCH (p)<-[b:Blocked]-(:User)
                    OPTIONAL MATCH (p)<-[f:Favourited]-(:User)
                    RETURN p as post,
                        u as creator,
                        collect(c) as comments,
                        collect(t) as tags,
                        COUNT(v) as views,
                        COUNT(f) as favourites,
                        COUNT(b) as blocked
                        """
        with driver.session() as tx:
            if id:
                response = tx.run(
                    "MATCH (p:Post { id:$id})" + query,
                    id=id).data()
            elif md5:
                response = tx.run(
                    "MATCH (p:Post { md5:$md5 })" + query,
                    md5=md5).data()
            else:
                raise ValueError(f"Must specify either id or md5: {id=} {md5=}")
        
        if not response:
            return None
        
        response = response[0]
        data = response['post']
        data['creator'] = response['creator']
        data['tags'] = response['tags']
        data['views'] = response['views']
        data['favourites'] = response['favourites']
        data['blocked'] = response['blocked']
        data['comments'] = response['comments']
            
        return data

    @staticmethod
    @measureTiming
    def search(*,tags:list=[],orderby:str='creation',direction:str='',limit:int=10):
        """
        Parameters:
            Ordering by
                views: By the view count of each post 
                creation: By the creation date of each post
            Limit: The number of posts to return
            Tags: A list of tags to search for
        """
        ordering = {
            "views":"views",
            "creation":"post.created",
            "id":"post.id",
            "md5":"post.md5"
            }
        with driver.session() as tx:
            response = tx.run(f"""
                    MATCH (post:Post)
                    MATCH (post)-[:Tagged]->(t:Tag)
                    WHERE t.name in $tags or $tags = []
                    RETURN post
                        ORDER BY $orderby
                        LIMIT $limit""",
                    tags=tags,limit=limit,orderby=ordering).data()
        
        posts = []
        for x in response:
            post = Post.get(id=x['post']['id'])
            if post:
                posts.append(post)
        return posts
    
    @staticmethod
    def delete(id:int):
        with driver.session() as tx:
            tx.run("""
                MATCH (n:Post {id:$id})
                DETACH DELETE n""",
                id=id)
