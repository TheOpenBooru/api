from . import db, create, exists
from modules import settings
from modules.database.Post import post_collection
from tqdm import tqdm
import logging
import time


def regenerate():
    logging.info("Started Regenerating Tags")
    start = time.time()
    cur = post_collection.aggregate(
        pipeline=[
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
            },
            {
                "$match":{
                    "count":{"$gt": settings.TAGS_MINIMUM_COUNT}
                }
            }
        ],
        batchSize=100,
    )
    tag_count = 0
    for doc in tqdm(cur,"Regenerating Tags"):
        tag_count += 1
        tag = doc['_id']
        count = doc['count']

        if count <= settings.TAGS_MINIMUM_COUNT:
            continue # Not important enough to be considered a tag
        
        if not exists(tag):
            create(tag,count=count)
        else:
            post_collection.update_one(
                filter={'name':tag},
                update={'$set':{'count':count}}
            )
    
    duration_ms = time.time() - start
    logging.info(f"Tag Regeneration: tags:{tag_count} time:{duration_ms:.3f}s")
