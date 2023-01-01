from . import parsing, iterable
from openbooru.modules import settings, schemas, database, posts
from openbooru.modules.importers import Importer, utils, DownloadFailure, run_importer
from typing import Union
from itertools import islice
from tqdm import tqdm
import requests
from openbooru.modules import settings


class E621Importer(Importer):
    _hostname = "e621.net"
    enabled = settings.IMPORTER_E621_ENABLED
    time_between_runs = settings.IMPORTER_E621_RETRY_AFTER
    def __init__(self):
        requests.get(f"https://{self._hostname}", timeout=2)


    async def load(self, limit:Union[int, None] = None):
        progress = tqdm(
            desc="Importing From E621 Dump",
            unit=" post",
            iterable=iterable.iter_over_posts(self._hostname),
            total=limit or iterable.guess_post_count(self._hostname),
        )
        await run_importer(
            iterable=progress,
            limit=limit,
            get_hashes=parsing.get_hashes,
            get_created_at=parsing.get_date,
            get_images=parsing.get_images,
            get_upvotes=parsing.get_upvotes,
            get_downvotes=parsing.get_downvotes,
            get_rating=parsing.get_rating,
            get_sources=parsing.get_sources(self._hostname),
            get_tags=parsing.get_tags,
        )

class E926Importer(E621Importer):
    _hostname = "e926.net"
    enabled = settings.IMPORTER_E621_ENABLED

