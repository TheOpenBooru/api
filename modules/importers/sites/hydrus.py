from modules import posts, settings, database, normalise
from modules.importers import Importer, utils
import logging
import requests
import hydrus_api
from tqdm import tqdm


class HydrusImporter(Importer):
    enabled: bool = settings.IMPORTER_HYDRUS_ENABLED
    time_between_runs = settings.IMPORTER_HYDRUS_RETRY_AFTER
    def __init__(self):
        requests.get(settings.IMPORTER_HYDRUS_URL,timeout=2)
        self.client = hydrus_api.Client(
            access_key=settings.IMPORTER_HYDRUS_KEY,
            api_url=settings.IMPORTER_HYDRUS_URL
        )
        self.client.get_api_version()


    async def load(self, limit: int|None = None):
        tags = settings.IMPORTER_HYDRUS_TAGS
        
        if type(limit) == int:
            tags.append(f"system:limit is {limit}")
        
        post_ids = self.client.search_files(
            tags,
            file_sort_type=hydrus_api.FileSortType.IMPORT_TIME,
        )
        post_ids = [int(id) for id in post_ids]
        
        post_metadata = []
        for x in range(int(len(post_ids) / 100)):
            start = x * 100
            end = start + 100
            metadata = self.client.get_file_metadata(file_ids=post_ids[start:end])
            post_metadata.extend(metadata)
        
        post_ids.reverse()
        post_metadata.reverse()
        
        zipped = list(zip(post_ids,post_metadata))
        for id,metadata in tqdm(zipped, desc="Importing From Hydrus"):
            try:
                await self._import_post(id,metadata)
            except Exception as e:
                logging.info(f"Hydrus Failed Import [{metadata['hash']}]: {e}")


    async def _import_post(self,post_id:int,metadata:dict):
        try:
            database.Post.sha256_get(metadata['hash'])
        except KeyError:
            pass
        else:
            return
        
        
        tags = set()
        for tag in extract_tags(metadata):
            sections = tag.split(':')
            if len(sections) == 2:
                _, tag = sections
            tags.update(tag)
        
        tags = normalise.normalise_tags(tags)
        sources = metadata['known_urls']
        
        r = self.client.get_file(file_id=post_id)
        try:
            post = await posts.create(
                data=r.content,
                filename="example" + metadata['ext'],
            )
        except posts.PostExistsException:
            return
        else:
            posts.edit(
                post_id=post.id,
                editter_id=None,
                tags=tags,
                sources=sources,
            )


def extract_tags(metadata:dict) -> list[str]:
    try:
        tag_lists = metadata['service_names_to_statuses_to_tags']['all known tags']
        all_tags = []
        for tags in tag_lists.values():
            all_tags.extend(tags)
        return all_tags
    except Exception:
        return []
