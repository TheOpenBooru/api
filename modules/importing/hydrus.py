from . import LocalImporter, _normalise_tags
from modules import posts, settings, database
from typing import Union
import hydrus_api
from tqdm import tqdm

class Hydrus(LocalImporter):
    enabled: bool = settings.IMPORT_HYDRUS_ENABLED
    def __init__(self):
        try:
            self.client = hydrus_api.Client(
                access_key=settings.IMPORT_HYDRUS_KEY,
                api_url=settings.IMPORT_HYDRUS_URL 
            )
        except Exception:
            self.functional = False
        else:
            self.functional = True


    async def import_default(self):
        ids = self.client.search_files(settings.IMPORT_HYDRUS_TAGS)
        metadatas = self.client.get_file_metadata(file_ids=ids) # type: ignore

        zipped = list(zip(ids,metadatas))
        for id,metadata in tqdm(zipped, desc="Importing From Hydrus"):
            await self._import_post(id,metadata)


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
        
        raw_tags = list(filter(lambda x:"source:" not in x,raw_tags))
        tags = _normalise_tags(raw_tags)
        
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
        tag_lists = metadata['service_names_to_statuses_to_tags']['all known tags']
        all_tags = []
        for tags in tag_lists.values():
            all_tags.extend(tags)
        return all_tags
