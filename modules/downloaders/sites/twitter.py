from . import Downloader, DownloadFailure, utils
from modules import settings, posts, schemas
from typing import Union
from collections import namedtuple
import re
import tweepy
from tweepy.client import Response


class Twitter(Downloader):
    enabled: bool = settings.DOWNLOADER_TWITTER_ENABLED
    client: tweepy.Client
    def __init__(self):
        self.client = tweepy.Client(bearer_token=settings.DOWNLOADER_TWITTER_KEY)


    def is_valid_url(self, url:str) -> bool:
        return bool(re.match(r"^https:\/\/twitter.com\/[a-zA-Z0-9_]+", url))


    async def download_url(self, url:str) -> list[schemas.Post]:
        account, id, photo = await parse_url(url)
        
        if account and id:
            if photo:
                photo_index = int(photo) - 1
            else:
                photo_index = None
            
            return await self.import_tweet(id, url, account, photo_index)
        else:
            raise DownloadFailure("Could Not Import Twitter URL")


    async def import_tweet(self, id:str, url:str, account:str, index:Union[int,None] = None) -> list[schemas.Post]:
        tweet = self.client.get_tweet(
            id=id,
            expansions="attachments.media_keys",
            media_fields="url,variants",
            tweet_fields="attachments,author_id",
        )
        if "media" not in tweet.includes:
            raise DownloadFailure("Post Doesn't Have Media")

        media_items = tweet.includes["media"]
        if index:
            media = media_items[index]
            return [await generate_from_media(media, url, account)]
        else:
            return [await generate_from_media(media, url, account) for media in media_items]



UrlData = namedtuple("UrlData", ["account", "id", "photo"])
async def parse_url(url:str) -> UrlData:
    ACCOUNT_REGEX = r"^https:\/\/twitter.com\/[a-zA-Z0-9_]+"
    ID_REGEX = ACCOUNT_REGEX + r"\/status\/[0-9]+"
    IMAGE_REGEX = ID_REGEX + r"\/photo\/[0-9]+"
    
    values = []
    for regex in (ACCOUNT_REGEX, ID_REGEX, IMAGE_REGEX):
        match =re.match(regex, url)
        if match == None:
            values.append(None)
        else:
            value = match.group().split('/')[-1]
            values.append(value)
    
    return UrlData(*values)


async def generate_from_media(media: tweepy.Media, source:str, account:str) -> schemas.Post:
    if media.type == "photo":
        file_url = media["url"]
    else:
        file_url = media.data['variants'][0]['url']
    
    data, filename = utils.download_url(file_url)
    post = await posts.generate(data,filename)

    post.source = source
    if account not in post.tags:
        post.tags.append(account.lower())

    return post
