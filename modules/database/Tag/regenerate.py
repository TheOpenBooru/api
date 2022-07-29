from . import db, create, exists
from tqdm import tqdm
import logging, time
from modules import settings

post_collection = db['posts']

def regenerate():
    start = time.time()
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
    docs = list(cur)
    for doc in tqdm(docs,"Regenerating Tags"):
        tag = doc['_id']
        count = doc['count']

        if count <= settings.TAGS_MINIMUM_COUNT:
            continue # Not important enough to be considered a tag
        
        if not exists(tag):
            create(tag,count=count)
        else:
            post_collection.update_many(
                filter={'name':tag},
                update={'$set':{'count':count}}
            )
    
    duration_ms = time.time() - start
    logging.info(f"Tag Regeneration: tags:{len(docs)} time:{duration_ms:.3f}s")
