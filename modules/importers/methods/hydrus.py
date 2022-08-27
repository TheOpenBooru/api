from . import Importer, utils
from modules import posts, settings, database
import logging
import requests
import hydrus_api
from tqdm import tqdm


class Hydrus(Importer):
    enabled: bool = settings.IMPORTER_HYDRUS_ENABLED
    def __init__(self):
        try:
            requests.get(settings.IMPORTER_HYDRUS_URL,timeout=2)
            self.client = hydrus_api.Client(
                access_key=settings.IMPORTER_HYDRUS_KEY,
                api_url=settings.IMPORTER_HYDRUS_URL
            )
            self.client.get_api_version()
        except Exception:
            self.functional = False
        else:
            self.functional = True


    async def load(self):
        ids = self.client.search_files(
            settings.IMPORTER_HYDRUS_TAGS,
            file_sort_type=hydrus_api.FileSortType.IMPORT_TIME,
        )
        metadatas = self.client.get_file_metadata(file_ids=ids) # type: ignore
        ids.reverse()
        metadatas.reverse()

        zipped = list(zip(ids,metadatas))
        for id,metadata in tqdm(zipped, desc="Importing From Hydrus"):
            try:
                id = int(id)
                await self._import_post(id,metadata)
            except Exception as e:
                logging.info(f"Hydrus Failed Import [{metadata['hash']}]: {e}")


    async def _import_post(self,post_id:int,metadata:dict):
        try:
            database.Post.getBySHA256(metadata['hash'])
        except KeyError:
            pass
        else:
            return
        
        raw_tags = await self._extract_tags(metadata)
        source = ""
        if metadata['known_urls']:
            source = metadata['known_urls'][0]
            # Prevent tweet importer linking to the twitter image
            if source.startswith("https://pbs.twimg.com/"): 
                source = metadata['known_urls'][1]
        
        tags = utils.normalise_tags(raw_tags)
        
        r = self.client.get_file(file_id=post_id)
        data = r.content
        filename = "example" + metadata['ext']
        try:
            await posts.create(
                data,
                filename,
                additional_tags=tags,
                source=source,
            )
        except posts.PostExistsException:
            pass


    async def _extract_tags(self,metadata:dict) -> list[str]:
        try:
            tag_lists = metadata['service_names_to_statuses_to_tags']['all known tags']
            all_tags = []
            for tags in tag_lists.values():
                all_tags.extend(tags)
            return all_tags
        except Exception:
            return []
