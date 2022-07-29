from modules.database import User


def toggleUpvote(user_id:int, post_id:int):
    user = User.get(user_id)
    if post_id in user.upvotes:
        User.remove_upvote(user_id,post_id)
    else:
        User.add_upvote(user_id,post_id)


def toggleDownvote(user_id:int, post_id:int):
    user = User.get(user_id)
    if post_id in user.downvotes:
        User.remove_downvote(user_id,post_id)
    else:
        User.add_downvote(user_id,post_id)