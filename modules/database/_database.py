from modules import settings
from pymongo.mongo_client import MongoClient as _MongoClient

db_client = _MongoClient(
    host=settings.MONGODB_HOSTNAME,
    port=settings.MONGODB_PORT,
    username=settings.MONGODB_USERNAME,
    password=settings.MONGODB_PASSWORD,
)

if settings.WIPE_ON_STARTUP:
    db_client.drop_database(settings.MONGODB_DB_NAME)

db = db_client[settings.MONGODB_DB_NAME]
