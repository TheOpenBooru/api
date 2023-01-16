from . import collection

def addUrl(id: int, url: str):
    collection.update_one(
        {'id': id},
        {'$push': {'urls': url}}
    )

def addUrls(id: int, urls: list[str]):
    collection.update_one(
        {'id': id},
        {'$push': {'urls': urls}}
    )
