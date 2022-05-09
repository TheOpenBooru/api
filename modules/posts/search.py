from modules import schemas,database,settings

async def search(query:schemas.Post_Query) -> list[schemas.Post]:
    query.limit = _validate_limit(query.limit)
    if query.limit == 0:
        return []
    _validate_sort(query.sort)
    return database.Post.search(query)

def _validate_limit(limit:int) -> int:
    if limit > settings.MAX_SEARCH_LIMIT:
        return settings.MAX_SEARCH_LIMIT
    elif limit < 0:
        return 0
    else:
        return limit

def _validate_sort(sort:str):
    ...