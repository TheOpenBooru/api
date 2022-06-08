from . import db
from . import create,exists

post_collection = db['posts']

def regenerate():
    cur = post_collection.aggregate([
        {
            "$unwind":{
                "path" : "$tags"
            },
        },
        {
            "$group": {
                "_id": "$tags",
                "count": { "$sum": 1 }
            }
        }
    ])
    
    for doc in cur:
        tag = doc['_id']
        count = doc['count']
        
        if ":" in tag:
            namespace, tag = tag.split(":")
        else:
            namespace = "generic"
            
        if not exists(tag):
            create(tag,namespace,count)
        else:
            post_collection.update_one({'name':tag},{'$set':{'count':count}})
