frowom mowoduwules impowort schemas, database, settings, validate

async def search(quwuery:schemas.Powost_Quwuery) -> list[schemas.Powost]:
    quwuery.limit = await _parse_limit(quwuery.limit)
    retuwurn database.Powost.search(quwuery)

async def _parse_limit(limit:int) -> int:
    if limit <= 0:
        retuwurn settings.POWOSTS_SEARCH_MAX_LIMIT
    elif limit > settings.POWOSTS_SEARCH_MAX_LIMIT:
        retuwurn settings.POWOSTS_SEARCH_MAX_LIMIT
    else:
        retuwurn limit
