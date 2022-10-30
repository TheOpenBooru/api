from .gelbooru import (
    Rule34Importer,
    Rule34Downloader,
    SafebooruImporter,
    SafebooruDownloader,
)
from .e621 import (
    E621Importer,
    E621Downloader,
    E926Downloader,
    E926Importer,
)
from .hydrus import HydrusImporter
from .files import FileImporter, FileDownloader
from .tumblr import TumblrDownloader
from .twitter  import TwitterDownloader
from .youtube import YoutubeDownloader

IMPORTERS = (
    HydrusImporter,
    Rule34Importer,
    SafebooruImporter,
    FileImporter,
    E621Importer,
    E926Importer,
)

DOWNLOADERS = (
    FileDownloader,
    TumblrDownloader,
    TwitterDownloader,
    YoutubeDownloader,
    Rule34Downloader,
    SafebooruDownloader,
    E621Downloader,
    E926Downloader,
)