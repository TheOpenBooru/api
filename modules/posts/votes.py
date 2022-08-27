from modules.database import User, Post

def add_upvote(post_id:int, user_id:int):
    _add_upvote(user_id, post_id)
    
    user = User.get(user_id)
    if id in user.upvotes:
        _remove_downvote(user.id, post_id)


def remove_upvote(post_id:int, user_id:int):
    user = User.get(user_id)
    if id in user.upvotes:
        _remove_upvote(user.id, post_id)


def add_downvote(post_id:int, user_id:int):
    _add_downvote(user_id, post_id)
    
    user = User.get(user_id)
    if id in user.upvotes:
        _remove_upvote(user.id, post_id)


def remove_downvote(post_id:int, user_id:int):
    user = User.get(user_id)
    if id in user.downvotes:
        _remove_downvote(user.id, post_id)



def _add_upvote(user_id:int, post_id:int):
    Post.add_upvote(post_id)
    User.add_upvote(user_id, post_id)


def _remove_upvote(user_id:int, post_id:int):
    Post.remove_upvote(post_id)
    User.remove_upvote(user_id, post_id)


def _add_downvote(user_id:int, post_id:int):
    Post.add_downvote(post_id)
    User.add_downvote(user_id, post_id)


def _remove_downvote(user_id:int, post_id:int):
    Post.remove_downvote(post_id)
    User.remove_downvote(user_id, post_id)
