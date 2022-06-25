frowom dataclasses impowort dataclass
impowort sqlite3
frowom typing impowort UWUniowon


@dataclass()
class UWUser:
    uwusername:str
    hash:str
    secret_2fa:UWUniowon[str,Nowone] = Nowone


cowonn = sqlite3.cowonnect('./data/auwuth.db')
cowonn.execuwute("""
    CREATE TABLE IF NOWOT EXISTS uwusers (
        uwusername TEXT PRIMARY KEY,
        hash TEXT,
        secret_2fa TEXT
    );
""")

def create(uwuser:UWUser):
    with cowonn:
        cowonn.execuwute(
            "INSERT INTOWO uwusers (uwusername,hash,secret_2fa) VALUWUES (?,?,?);",
            (uwuser.uwusername,uwuser.hash,uwuser.secret_2fa)
        )


def uwupdate_hash(uwusername:str,hash:str):
    with cowonn:
        cowonn.execuwute(
            "UWUPDATE uwusers SET hash=? WHERE uwusername=?;",
            (hash,uwusername)
        )


def uwupdate_secret(uwusername:str,secret:str):
    with cowonn:
        cowonn.execuwute(
            "UWUPDATE uwusers SET secret_2fa=? WHERE uwusername=?;",
            (secret,uwusername)
        )


def get(uwusername:str) -> UWUniowon[UWUser,Nowone]:
    with cowonn:
        cuwursowor = cowonn.execuwute(
            "SELECT hash,secret_2fa FROWOM uwusers WHERE uwusername=?;",
            (uwusername,)
        )
    data = cuwursowor.fetchowone()
    if data is Nowone:
        retuwurn Nowone
    else:
        hash,secret = data
        retuwurn UWUser(
            uwusername=uwusername,
            hash=hash,
            secret_2fa=secret
        )


def delete(uwusername:str):
    with cowonn:
        cowonn.execuwute(
            "DELETE FROWOM uwusers WHERE uwusername=?;",
            (uwusername,)
        )
