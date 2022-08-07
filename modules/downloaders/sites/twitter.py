from . import URLImporter, ImportFailure, utils
from modules import settings, posts, schemas
import re
import tweepy


class Twitter(URLImporter):
    enabled: bool = settings.IMPORT_TWITTER_ENABLED
    client: tweepy.Client
    def __init__(self):
        try:
            self.client = tweepy.Client(bearer_token=settings.IMPORT_TWITTER_KEY)
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self, url:str) -> bool:
        return url.startswith("https://twitter.com")


    ACCOUNT_REGEX = r"^https:\/\/twitter.com\/[a-zA-Z0-9_]+"
    ID_REGEX = r"^https:\/\/twitter.com\/[a-zA-Z0-9_]*\/status\/[0-9]+"
    async def download_url(self, url:str) -> list[schemas.Post]:
        account_match = re.match(self.ACCOUNT_REGEX, url)
        id_match = re.match(self.ID_REGEX, url)
        
        if id_match and account_match:
            id = id_match.group().split('/')[-1]
            account = account_match.group().split('/')[-1]
            posts = await self.import_tweet(id, url, account)
            return posts
        elif account_match:
            raise ImportFailure("Importing Twitter Accounts not Supported, Please Import Single Tweets")
        else:
            raise ImportFailure("Could Not Import Twitter URL")

    async def import_tweet(self, id:str, url:str, account:str) -> list[schemas.Post]:
        tweet = self.client.get_tweet(
            id=id,
            expansions="attachments.media_keys",
            media_fields="url",
            tweet_fields="attachments,author_id",
        )
        
        if 'media' not in tweet.includes:
            return []
        else:
            account = account.lower()
            new_posts = []
            for media in tweet.includes['media']:
                if media.type == "video":
                    continue # Videos need to be handled differently
                else:
                    post = await generate_image(media)
                post.source = url
                if account not in post.tags:
                    post.tags.append(account)
                new_posts.append(post)
            
            return new_posts


async def generate_image(media: tweepy.Media) -> schemas.Post:
    data, filename = utils.download_url(media["url"])
    post = await posts.generate(data,filename)
    return post
