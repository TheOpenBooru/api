from modules import settings
from pymongo.mongo_client import MongoClient as _MongoClient

if settings.MONGODB_USERNAME:
    TEMPLATE_URL = "mongodb://{user}@{host}:{port}"
elif settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD:
    TEMPLATE_URL = "mongodb://{user}:{_pass}@{host}:{port}"
else:
    TEMPLATE_URL = "mongodb://{host}:{port}"

url = TEMPLATE_URL.format(
    host=settings.MONGODB_HOSTNAME,
    port=settings.MONGODB_PORT,
    user=settings.MONGODB_USERNAME,
    _pass=settings.MONGODB_PASSWORD,
)
db_client: _MongoClient = _MongoClient(url)

if settings.WIPE_ON_STARTUP:
    db_client.drop_database(settings.MONGODB_DB_NAME)

db = db_client[settings.MONGODB_DB_NAME]
