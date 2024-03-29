from . import Post, post_collection, encode_post

def update(id:int,new_version:Post):
    """Raises:
    - KeyError: Post not found
    """
    document = encode_post(new_version)
    res = post_collection.find_one_and_replace(
        filter={'id':id},
        replacement=document,
        return_document=True,
    )
    if res == None:
        raise KeyError("Post not found")