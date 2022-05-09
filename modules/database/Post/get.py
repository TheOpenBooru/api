from . import Post,post_collection

def get(id:int) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    document = post_collection.find_one({'id':id})
    if document == None:
        raise KeyError("Could not find post")
    else:
        post = Post.parse_obj(document)
        return post