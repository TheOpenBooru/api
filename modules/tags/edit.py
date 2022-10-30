from modules import database, schemas, settings

class TagEditFailure(Exception):
    message:str
    def __init__(self, msg:str):
        self.message = msg


async def edit(
        tag_name:str,
        namespace:str|None = None,
        siblings:list|None = None,
        parents:list|None = None,
        valid_namespaces:list[str] = settings.TAGS_NAMESPACES
    ) -> schemas.Tag:

    if namespace not in valid_namespaces:
        raise TagEditFailure("An Invalid Namespace was Provided")

    try:
        tag = database.Tag.get(tag_name)
    except KeyError:
        raise TagEditFailure("That Tag Does Not Exist")
    
    new_tag = tag.copy()
    new_tag.namespace = namespace or tag.namespace
    new_tag.siblings = siblings or tag.siblings
    new_tag.parents = parents or tag.parents

    if tag == new_tag:
        raise TagEditFailure("No Changes Were Made")
    
    database.Tag.update(tag_name, new_tag)
    
    return new_tag
