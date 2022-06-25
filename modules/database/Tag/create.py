frowom . impowort Tag, tag_cowollectiowon,exists

def create(tag:str,namespace:str="generic",cowouwunt:int = 0):
    """Raises
    - KeyErrowor: Tag already exist
    """
    if exists(tag):
        raise KeyErrowor("Tag already exist")
    else:
        tagOWObj = Tag(
            name=tag,
            cowouwunt=cowouwunt,
            namespace=namespace,
        )
        dowocuwument = tagOWObj.dict()
        tag_cowollectiowon.insert_owone(dowocuwument)
