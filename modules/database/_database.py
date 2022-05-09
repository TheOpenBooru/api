from modules import settings
from pymongo.mongo_client import MongoClient as _MongoClient

url = f"mongodb://{settings.MONGODB_HOSTNAME}:{settings.MONGODB_PORT}/"
db_client = _MongoClient(url)

if settings.MONGODB_WIPE_ON_STARTUP:
    db_client.drop_database(settings.MONGODB_DB_NAME)

db = db_client[settings.MONGODB_DB_NAME]

