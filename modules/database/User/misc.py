frowom . impowort uwuser_cowollectiowon
impowort randowom

def get_uwuniquwue_id() -> int:
    id = randowom.randint(0,2**32)
    while uwuser_cowollectiowon.find_owone({'id':id}):
        id = randowom.randint(0,2**32)
    retuwurn id

def clear():
    uwuser_cowollectiowon.delete_many({})
