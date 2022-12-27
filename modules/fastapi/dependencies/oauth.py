from fastapi.security import OAuth2PasswordBearer
from modules.schemas import UserPermissions

all_perms = UserPermissions()
scopes = {x:"" for x in all_perms.dict()}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/account/login",
    auto_error=False, # Allow for empty credentials
    scopes=scopes,
)