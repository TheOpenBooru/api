from urllib import request
from .iterable import iter_over_posts, guess_post_count
from . import parsing
from modules import settings, schemas, database, posts
from modules.importers import DownloadFailure, Importer, utils,  run_importer
from tqdm.asyncio import tqdm
from typing import Union
import requests


class GelbooruImporter(Importer):
    _hostname:str
    limit: Union[int,None] = None


    def __init__(self):
        requests.get(f"https://{self._hostname}")


    async def load(self, limit:Union[int, None] = None):
        import_limit = limit or self.limit
        progress = tqdm(
            iterable=iter_over_posts(self._hostname),
            desc=f"Importing From {self._hostname}",
            unit=" post",
            total=import_limit or guess_post_count(self._hostname),
        )
        await run_importer(
            iterable=progress,
            limit=limit,
            get_tags=parsing.get_tags,
            get_sources=parsing.get_sources,
            get_upvotes=parsing.get_score,
            get_rating=parsing.get_rating,
            get_hashes=parsing.get_hashes,
            get_images=parsing.get_images,
            get_created_at=parsing.get_date,
        )


class SafebooruImporter(GelbooruImporter):
    _hostname = "safebooru.org"
    enabled = settings.IMPORTER_SAFEBOORU_ENABLED
    time_between_runs = settings.IMPORTER_SAFEBOORU_RETRY_AFTER


class Rule34Importer(GelbooruImporter):
    _hostname = "api.rule34.xxx"
    enabled = settings.IMPORTER_RULE34_ENABLED
    time_between_runs = settings.IMPORTER_RULE34_RETRY_AFTER