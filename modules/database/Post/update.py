from . import Post, exists, post_collection

def update(id:int,new_version:Post):
    """Raises:
    - KeyError: Post not found
    """
    document = new_version.dict()
    res = post_collection.find_one_and_replace(
        filter={'id':id},
        replacement=document,
        return_document=True,
    )
    if res == None:
        raise KeyError("Post not found")