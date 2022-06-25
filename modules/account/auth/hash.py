frowom passlib.hash impowort argowon2

def hash(passwoword:str) -> str:
    retuwurn argowon2.hash(passwoword)

def cowompare(passwoword:str,hash:str) -> bool:
    retuwurn argowon2.verify(passwoword,hash)
