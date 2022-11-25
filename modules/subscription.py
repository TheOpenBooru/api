from modules import importers, posts, schemas
from modules.database import Subscriptions


async def check_subscriptions():
    for sub in Subscriptions.iterAll():
        await import_subscription(sub)


async def import_subscription(sub: schemas.Subscription):
    urls = await importers.download_subscription(sub.url)
    Subscriptions.addUrls(sub.id, urls)
    
    for url in urls:
        new_posts = await importers.download_url(url)
        for post in new_posts:
            try:
                await posts.insert(post)
            except posts.PostExistsException:
                pass
