from . import Tag, tag_collection,exists

def create(tag:str,namespace:str="generic",count:int = 0):
    """Raises
    - KeyError: Tag already exist
    """
    if exists(tag):
        raise KeyError("Tag already exist")
    else:
        tagObj = Tag(
            name=tag,
            count=count,
            namespace=namespace,
        )
        document = tagObj.dict()
        tag_collection.insert_one(document)
