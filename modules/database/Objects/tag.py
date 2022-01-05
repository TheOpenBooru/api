from . import db_run,combine_kwargs
from cachetools import cached,TTLCache

DATA_QUERY = """
    MATCH (n:Tag)-[:Tagged]->(p:Post)
    RETURN
        n.created_at as created_at,
        n.name as name,
        n.namespace as namespace,
        COUNT(n) as count
"""

class Tag:
    @staticmethod
    def create(name:str,namespace:str):
        db_run("""
            CREATE (t:Tag {
                created_at:timestamp(),
                name:$name,
                namespace:$namespace
            })
        """)


    @staticmethod
    def get(name:str) -> dict:
        query = "MATCH (t:Tag) WHERE t.name = $name" + DATA_QUERY
        data = db_run(query,name=name)
        
        if not data:
            raise KeyError("Tag with that Name could not be found")
        else:
            return data[0]


    @staticmethod
    def search(limit:int=32,order:str='count',**kwargs) -> list[dict]:
        """Search for tags based on the keyword arguments
        
        Args:
            limit: The maximum number of results to return
            order: Ordered by... 'count','name'
        
        Kwargs:
            name (str): The name of the tag
            namespace (str): The namespace of the tag
            
        Raises:
            ValueError: Invalid kwarg key or invalid order
            TypeError:  Invalid kwarg type
        """
        ORDERS = {
            'count':'n.count',
            'name':'n.name',
        }
        LOOKUP = {
            "name_regex": [str,"WHERE n.name ~= $name_regex"],
            "namespace" : [str,"WHERE n.namespace = $namespace"],
            "before"    : [int,"WHERE n.created_at < $before"],
            "after"     : [int,"WHERE n.created_at > $after"],
        }
        
        if order not in ORDERS:
            raise ValueError("Invalid Order Parameter")
        
        query = "MATCH (n:Tag)"
        query += combine_kwargs(LOOKUP,kwargs)
        query += DATA_QUERY + f"ORDER BY {ORDERS[order]}" + "LIMIT $limit"
        
        return db_run(query,limit=limit,**kwargs)


    @staticmethod
    def set(name:str,**kwargs):
        """Set a Tag's properties
        
        Kwargs:
            name (str): The name of the tag
            namespace (str): The namespace of the tag
            
        Raises:
            ValueError: Invalid kwarg key or invalid order
            TypeError:  Invalid kwarg type
        """
        LOOKUP = {
            "name"      : [str,"SET n.name = $name"],
            "namespace" : [str,"SET n.namespace = $namespace"],
        }
        
        query = "MATCH (n:Tag) WHERE n.name = $name"
        query += combine_kwargs(LOOKUP,kwargs)
        
        db_run(query,name=name,**kwargs)

        
    @staticmethod
    @cached(cache=TTLCache(maxsize=1,ttl=60*60*24*7))
    def list_all() -> list[dict]:
        return db_run("MATCH (n:Tag) " + DATA_QUERY)
    
    @staticmethod
    def delete(name:str):
        db_run(
            "MATCH (n:Tag) WHERE n.name = $name DELETE n",
            name=name
        )