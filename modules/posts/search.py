from modules import schemas,database,settings

async def search(query:schemas.Post_Query) -> list[schemas.Post]:
    return database.Post.search(query)
