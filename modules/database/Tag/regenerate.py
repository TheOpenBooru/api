from . import tag_collection, create, exists
from modules import settings, schemas
from modules.database.Post import post_collection
from typing import Union
from tqdm import tqdm
import logging
from pymongo.command_cursor import CommandCursor
import time



def regenerate_count(min_count:int = settings.TAGS_MINIMUM_COUNT):
    start = time.time()

    tag_data = getTagData(min_count)
    for doc in tqdm(tag_data,"Regenerating Tags"):
        name, count = doc
        
        if not exists(name):
            create(name,count=count)
        else:
            tag_collection.update_one(
                filter={'name':name},
                update={'$set':{'count':count}}
            )
    
    duration_ms = time.time() - start
    logging.info(f"Tag Regeneration: tags:{len(tag_data)} time:{duration_ms:.3f}s")


tag, count = str, int
def getTagData(min_count: int) -> list[tuple[tag, count]]:
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
    ]

    if min_count:
        pipeline.append(
            {
                "$match": {
                    "count":{"$gt": min_count}
                }
            }
        )
    
    cur = post_collection.aggregate(pipeline=pipeline)
    tag_data = [(doc['_id'], doc['count']) for doc in cur]
    return tag_data