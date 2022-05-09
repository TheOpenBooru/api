from . import post_collection,exists

def increment_view(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'views':1}}, # Increment views by 1
    )
