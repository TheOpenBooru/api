from . import db,Tag

tag_collection = db['tags']

# Indexes
tag_collection.create_index('name', unique=True)
tag_collection.create_index('created_at')
tag_collection.create_index('count')
tag_collection.create_index('namespace')
tag_collection.create_index('siblings')
tag_collection.create_index('parents')