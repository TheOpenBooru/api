from modules.database import User, Post

def add_upvote(post_id, user_id):
    user = User.get(user_id)
    if id in user.upvotes:
        Post.remove_downvote(post_id)
        User.remove_downvote(user.id, post_id)
    
    Post.add_upvote(post_id)
    User.add_upvote(user.id, post_id)


def remove_upvote(post_id, user_id):
    user = User.get(user_id)
    if id in user.upvotes:
        Post.remove_upvote(post_id)
        User.remove_upvote(user.id, post_id)


def add_downvote(post_id, user_id):
    user = User.get(user_id)
    if id in user.upvotes:
        Post.remove_upvote(post_id)
        User.remove_upvote(user.id, post_id)
    
    Post.add_downvote(post_id)
    User.add_downvote(user.id, post_id)


def remove_downvote(post_id, user_id):
    user = User.get(user_id)
    if id in user.downvotes:
        Post.remove_downvote(post_id)
        User.remove_downvote(user.id, post_id)
