from modules import schemas, database, settings, validate

DEFAULT_QUERY = schemas.PostQuery()
async def search(query:schemas.PostQuery = DEFAULT_QUERY) -> list[schemas.Post]:
    parsed_query = query.copy()
    parsed_query.limit = _parse_limit(parsed_query.limit)
    return database.Post.search(parsed_query)


def _parse_limit(limit:int) -> int:
    limit = min(limit, settings.POSTS_SEARCH_MAX_LIMIT)
    limit = max(limit, 1)
    return limit
