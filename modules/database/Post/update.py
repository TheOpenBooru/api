from . import Post, exists, post_collection

def update(id:int,new_version:Post):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")
    else:
        document = new_version.dict()
        post_collection.replace_one(
            filter={'id':id},
            replacement=document
        )