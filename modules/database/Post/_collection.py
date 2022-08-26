from . import db

post_collection = db['posts']

# Indexes
post_collection.create_index('id', unique=True)
post_collection.create_index('created_at')
post_collection.create_index('tags')
post_collection.create_index('hashes.md5s')
post_collection.create_index('hashes.sha256s')
post_collection.create_index('hashes.phashs')
post_collection.create_index('source')
post_collection.create_index('uploader')
post_collection.create_index('media_type')
post_collection.create_index('views')
post_collection.create_index('upvotes')
post_collection.create_index('downvotes')
