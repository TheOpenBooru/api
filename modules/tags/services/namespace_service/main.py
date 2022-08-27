from . import get_rule34_namespace
from modules import settings

def get_tag_namespace(tag:str) -> str:
    r34_namespace = get_rule34_namespace(tag)
    if r34_namespace in settings.TAGS_NAMESPACES:
        return r34_namespace

    return "generic"