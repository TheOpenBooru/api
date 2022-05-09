from . import db

post_collection = db['posts']

# Indexes
post_collection.create_index('id')
post_collection.create_index('uploader')
post_collection.create_index('created_at')
post_collection.create_index('media_type')
post_collection.create_index('views')
post_collection.create_index('upvotes')
post_collection.create_index('downvotes')
