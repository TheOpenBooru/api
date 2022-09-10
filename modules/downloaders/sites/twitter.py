from typing import Union
from . import Downloader, DownloadFailure, utils
from modules import settings, posts, schemas
import re
import tweepy


class Twitter(Downloader):
    enabled: bool = settings.DOWNLOADER_TWITTER_ENABLED
    client: tweepy.Client
    def __init__(self):
        try:
            self.client = tweepy.Client(bearer_token=settings.DOWNLOADER_TWITTER_KEY)
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self, url:str) -> bool:
        return bool(re.match(r"^https:\/\/twitter.com\/[a-zA-Z0-9_]+", url))


    ACCOUNT_REGEX = r"^https:\/\/twitter.com\/[a-zA-Z0-9_]+"
    ID_REGEX = r"^https:\/\/twitter.com\/[a-zA-Z0-9_]*\/status\/[0-9]+"
    IMAGE_REGEX = r"^^https:\/\/twitter.com\/[a-zA-Z0-9_]*\/status\/[0-9]+\/photo\/[0-9]+"
    async def download_url(self, url:str) -> list[schemas.Post]:
        account_match = re.match(self.ACCOUNT_REGEX, url)
        id_match = re.match(self.ID_REGEX, url)
        image_match = re.match(self.IMAGE_REGEX, url)
        
        if id_match and account_match:
            id = id_match.group().split('/')[-1]
            account = account_match.group().split('/')[-1]
            
            if image_match:
                index_string = image_match.group().split('/')[-1]
                photo_index = int(index_string) - 1
                return await self.import_tweet(id, url, account, photo_index)
            else:
                return await self.import_tweet(id, url, account)
        else:
            raise DownloadFailure("Could Not Import Twitter URL")


    async def import_tweet(self, id:str, url:str, account:str, index:Union[int,None] = None) -> list[schemas.Post]:
        tweet = self.client.get_tweet(
            id=id,
            expansions="attachments.media_keys",
            media_fields="url",
            tweet_fields="attachments,author_id",
        )
        if "media" not in tweet.includes:
            raise DownloadFailure("Post Doesn't Have Media")

        medias = tweet.includes["media"]
        if index:
            media = medias[index]
            post = await generate_from_media(media, url, account)
            return [post]
        else:
            new_posts = []
            for media in medias:
                post = await generate_from_media(media, url, account)
                new_posts.append(post)

            return new_posts


async def generate_from_media(media: tweepy.Media, url:str, account:str) -> schemas.Post:
    if media.type == "video":
        post = await generate_video(media)
    elif media.type == "animated_gif":
        post = await generate_gif(media)
    else:
        post = await generate_image(media)

    post.source = url
    if account not in post.tags:
        post.tags.append(account.lower())

    return post


async def generate_image(media: tweepy.Media) -> schemas.Post:
    data, filename = utils.download_url(media["url"])
    post = await posts.generate(data,filename)
    return post


async def generate_gif(media: tweepy.Media) -> schemas.Post:
    raise DownloadFailure("Twitter Gifs Not Supported")


async def generate_video(media: tweepy.Media) -> schemas.Post:
    raise DownloadFailure("Twitter Video Not Supported")