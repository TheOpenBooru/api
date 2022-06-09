from . import user_collection

def createPost(user_id:int, post_id:int):
    user_collection.update_one({'id':user_id},{'$push':{'posts':post_id}})
