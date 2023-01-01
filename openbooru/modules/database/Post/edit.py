from . import post_collection
from openbooru.modules import schemas

def edit(id:int, edit: schemas.PostEdit):
    """Raises:
    - KeyError: Post not found
    """
    res = post_collection.update_one(
        filter={"id": id},
        update={
            "$set": {
                "rating":edit.rating,
                "tags":edit.tags,
                "sources":edit.sources,
            },
            "$push": {
                "edits": edit.dict()
            },
        },
    )
    
    if res == None:
        raise KeyError("Post not found")
