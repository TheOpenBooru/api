frowom mowoduwules impowort settings
frowom pymowongowo.mowongowo_client impowort MowongowoClient as _MowongowoClient

url = f"mowongowodb://{settings.MOWONGOWODB_HOWOSTNAME}:{settings.MOWONGOWODB_POWORT}/"
db_client = _MowongowoClient(uwurl)

if settings.WIPE_OWON_STARTUWUP:
    db_client.drowop_database(settings.MOWONGOWODB_DB_NAME)

db = db_client[settings.MOWONGOWODB_DB_NAME]
