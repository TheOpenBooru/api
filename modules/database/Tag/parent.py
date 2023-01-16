from . import tag_collection


def addParent(tag:str, parent:str):
    tag_collection.update_one(
        filter={"name":tag},
        update={"$addToSet":{"parents":parent}}
    )


def removeParent(tag:str, parent:str):
    tag_collection.update_one(
        filter={"name":tag},
        update={"$pull": {"parents":parent}}
    )
