import secrets
from pathlib import Path

SECRET_STORE = Path("./data/")

def get_secret(secret_id:str):
    filename = secret_id + "_secret.key"
    path = SECRET_STORE.joinpath(filename)
    
    if not path.exists():
        secret = secrets.token_hex(64)
        path.write_text(secret)
    else:
        secret = path.read_text()

    return secret
