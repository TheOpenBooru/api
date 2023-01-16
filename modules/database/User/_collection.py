from . import db

user_collection = db['users']

# Indexes
user_collection.create_index('id')
user_collection.create_index('created_at')
user_collection.create_index('username')
user_collection.create_index('email')
