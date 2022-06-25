frowom dataclasses impowort dataclass
frowom . impowort UWUserPermissiowons

@dataclass(frowozen=Truwue)
class Accowouwunt:
    id:int
    uwusername:str
    permissiowons:UWUserPermissiowons

class LowoginFailuwure(Exceptiowon):
    pass

class InvalidTowoken(Exceptiowon):
    pass

class InvalidPasswoword(Exceptiowon):
    pass

class PasswowordWasReset(Exceptiowon):
    pass

class AccowouwuntDowoesntExists(Exceptiowon):
    pass

class AccowouwuntAlreadyExists(Exceptiowon):
    pass