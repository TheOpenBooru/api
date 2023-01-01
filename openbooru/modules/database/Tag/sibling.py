from . import tag_collection


def addSibling(tag:str, sibling:str):
    tag_collection.update_one(
        filter={"name":tag},
        update={"$addToSet":{"siblings":sibling}}
    )


def removeSibling(tag:str, sibling:str):
    tag_collection.update_one(
        filter={"name":tag},
        update={"$pull": {"siblings":sibling}}
    )
