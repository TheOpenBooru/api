from modules import settings
from modules.normalisation import normalise_tags
import logging
import requests
import io


def generate_ai_tags(data:bytes, filename:str, mimetype:str) -> list[str]:
    buf = io.BytesIO(data)
    try:
        r = requests.post(
            url=settings.TAGS_TAGGING_SERVICE_URL,
            files=[('file', (filename, buf, mimetype))],
            timeout=20,
        )
    except Exception:
        logging.warning("Tagging Service Timed Out. Is it down?")
        settings.TAGS_TAGGING_SERVICE_ENABLED = False
        return []

    try:
        tags = r.json()
        tags = normalise_tags(tags)
        return tags
    except Exception:
        return []
