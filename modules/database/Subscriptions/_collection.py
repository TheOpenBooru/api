from . import db

collection = db["subscriptions"]

# Indexes
collection.create_index("id", unique=True)
collection.create_index("created_at")
collection.create_index("url", unique=True)
collection.create_index("creator")