from openbooru.modules import importers
from openbooru.modules.schemas import MediaType, Rating
from dataclasses import dataclass
import pytest

test_data = [
    (
        importers.E621Downloader,
        (
            ("https://e621.net/posts/2294957", "Should accept post link"),
            ("https://e621.net/posts/2294957?q=test", "Should accept query string"),
        ),
        (
            ("http://e926.net/posts/2294957", "Should not accept non-e621 links"),
            ("http://e621.net/posts/2294957", "Should not accept http link"),
            ("https://e621.net/posts/", "Should not accept /posts link"),
        )
    ),
    (
        importers.Rule34Downloader,
        (
            ("https://rule34.xxx/index.php?page=post&s=view&id=5198120", "Should accept post link"),
            ("https://rule34.xxx/index.php?page=post&s=view&id=5198120&test=1", "Should accept query param"),
        ),
        (
            ("https://safebooru.org/index.php?page=post&s=view&id=5198120","Should not accept non-rule34 page"),
            ("http://rule34.xxx/index.php?page=post&s=view","Should not accept post view page"),
            ("https://rule34.xxx/index.php?page=post&s=view","Should not accept http link"),
            ("https://rule34.xxx/index.php?page=post&s=list","Should not accept post list page"),
            ("https://rule34.xxx/index.php?page=pool&s=show&id=21185","Should not accept show page with id"),
        )
    ),
]

@pytest.mark.parametrize(("downloader", "valid_urls", "invalid_urls"), test_data,)
def test_is_valid_url(
        downloader: type[importers.Downloader],
        valid_urls:list[tuple[str, str]],
        invalid_urls:list[tuple[str, str]],
        ):
    _downloader = downloader()
    for url, reason in valid_urls:
        assert _downloader.is_valid_url(url), reason
    
    for url, reason in invalid_urls:
        assert not _downloader.is_valid_url(url), reason

