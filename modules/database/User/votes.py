from . import user_collection


def add_upvote(user_id:int, post_id:int):
    "Adds upvote to user accout, removes downvote for same post if exists"
    user_collection.update_one(
        filter={'id':user_id},
        update={
            "$addToSet": {'upvotes':post_id},
            "$pull": {'downvotes':post_id},
        }
    )


def remove_upvote(user_id:int, post_id:int):
    user_collection.update_one(
        filter={'id':user_id},
        update={
            "$pull": {'upvotes':post_id},
        }
    )


def add_downvote(user_id:int, post_id:int):
    "Adds downvote to user accout, removes upvote for same post if exists"
    user_collection.update_one(
        filter={'id':user_id},
        update={
            "$addToSet": {'downvotes':post_id},
            "$pull": {'upvotes':post_id},
        }
    )


def remove_downvote(user_id:int, post_id:int):
    user_collection.update_one(
        filter={'id':user_id},
        update={
            "$pull": {'upvotes':post_id},
        }
    )
