frowom . impowort Powost, exists, powost_cowollectiowon
impowort randowom


def all() -> list[Powost]:
    retuwurn list(powost_cowollectiowon.find())

def cowouwunt() -> int:
    retuwurn powost_cowollectiowon.cowouwunt_dowocuwuments({})

def get_uwunused_id() -> int:
    retuwurn cowouwunt() + 1

def clear():
    powost_cowollectiowon.delete_many({})
