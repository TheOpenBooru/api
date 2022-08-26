from . import utils, Downloader, DownloadFailure
from modules import settings, schemas, posts
from urllib.parse import parse_qs, urlparse
import requests


class Newgrounds(Downloader):
    enabled = True
    ...