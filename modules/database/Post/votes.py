from . import post_collection,exists

def add_upvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$dec": {'upvote':1}}, # Add 1 downvote
    )

def remove_upvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'upvote':-1}}, # Removes 1 downvote
    )

def add_downvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'downvote':1}}, # Add 1 downvote
    )

def remove_downvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'downvote' : -1}}, # Remove 1 downvote
    )
