from modules import schemas, database, settings, validate

async def search(query:schemas.Post_Query) -> list[schemas.Post]:
    query.limit = _parse_limit(query.limit)
    return database.Post.search(query)

def _parse_limit(limit:int) -> int:
    if limit <= 0:
        return settings.POSTS_SEARCH_MAX_LIMIT
    elif limit > settings.POSTS_SEARCH_MAX_LIMIT:
        return settings.POSTS_SEARCH_MAX_LIMIT
    else:
        return limit
