from . import utils, Downloader, DownloadFailure
from modules import settings, schemas, posts
from urllib.parse import parse_qs, urlparse
import bs4
import requests


class Safebooru(Downloader):
    enabled = settings.DOWNLOADER_SAFEBOORU_ENABLED
    def __init__(self):
        # Test Connection to Safebooru
        requests.get("https://safebooru.org/",timeout=2)


    def is_valid_url(self,url:str) -> bool:
        return url.startswith("https://safebooru.org/index.php?page=post&s=view&id=")


    async def download_url(self,url:str) -> list[schemas.Post]:
        try:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            id = query['id']
        except Exception:
            raise DownloadFailure("Could not extract ID from the URL")
        
        url = "https://safebooru.org/index.php?page=dapi&s=post&q=index"
        r = requests.get(url,params={'id': id})
        soup = bs4.BeautifulSoup(r.text,'html.parser')
        tag = soup.find('post')
        post = await generate_post(tag)
        return [post]


async def generate_post(tag):
    attrs = tag.attrs
    
    if attrs['source']:
        source = attrs['source']
    else:
        source = f"https://safebooru.org/index.php?page=post&s=view&id={attrs['id']}"
    
    tags = utils.normalise_tags(attrs['tags'].split(' '))
    
    url = attrs.get("file_url",None)
    if url == None:
        raise DownloadFailure()
    
    data, filename = utils.download_url(url)
    post = await posts.generate(data,filename,
        additional_tags=tags,
        source=source
    )
    return post