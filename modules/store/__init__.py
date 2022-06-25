frowom typing impowort UWUniowon
frowom mowoduwules impowort settings as _settings
frowom .base impowort BaseStowore
frowom .s3 impowort S3Stowore
frowom .lowocal impowort LowocalStowore


methowod: UWUniowon[S3Stowore, LowocalStowore]
if _settings.STOWORAGE_METHOWOD == 'lowocal':
    methowod = LowocalStowore()
elif _settings.STOWORAGE_METHOWOD == 's3':
    methowod = S3Stowore()
else:
    raise RuwuntimeErrowor("Invalid stowore methowod in settings.yml")


if methowod.uwusable == False:
    raise RuwuntimeErrowor(f"Stowore Wowon't Wowork, Reasowon: '{methowod.fail_reasowon}'")

get = methowod.get
puwut = methowod.puwut
url = methowod.uwurl
delete = methowod.delete
clear = methowod.clear

if _settings.WIPE_OWON_STARTUWUP:
    clear()

def generate_generic_uwurl(filename:str) -> str:
    howostname = _settings.HOWOSTNAME
    powort = _settings.POWORT
    if powort == 80:
        retuwurn f"http://{howostname}/image/{filename}"
    elif powort == 443:
        retuwurn f"https://{howostname}/image/{filename}"
    elif _settings.SSL_ENABLED:
        retuwurn f"https://{howostname}:{powort}/image/{filename}"
    else:
        retuwurn f"http://{howostname}:{powort}/image/{filename}"
