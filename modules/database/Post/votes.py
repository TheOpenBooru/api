from . import post_collection,exists

def add_upvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'upvote':1}},
    )

def remove_upvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'upvote':-1}},
        # MongoDB has no decrement, so increment by -1
    )

def add_downvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'downvote':1}},
    )

def remove_downvote(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if not exists(id):
        raise KeyError("Post not found")

    post_collection.update_one(
        filter={'id':id},
        update={"$inc": {'downvote' : -1}},
    )
