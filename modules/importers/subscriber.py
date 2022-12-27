from .sites import SUBSCRIBERS


async def download_subscription(url: str) -> list[str]:
    for subscriber in SUBSCRIBERS:
        if subscriber.is_valid_url(url):
            break

    return []
