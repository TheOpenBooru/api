import string
import os
import bs4
from modules import validate


_VALID_CHARS = string.ascii_lowercase + string.digits + '_()'

def _normalise_tags(tags:list[str]) -> list[str]:
    if " " in tags:
        tags.remove(" ")

    tags = [_normalise_tag(tag) for tag in tags]
    tags = list(filter(validate.tag,tags))
    tags = list(set(tags))
    return tags


def _normalise_tag(tag:str) -> str:
    sections = tag.split(':')
    if len(sections) == 2:
        tag = sections[1]
    
    tag = tag.strip('\n')
    tag = tag.replace(' ','_')
    tag_chars = list(tag)
    
    filter_func = lambda chr: chr in _VALID_CHARS
    filtered_chars = list(filter(filter_func,tag_chars))
    tag = ''.join(filtered_chars)
    
    return tag


def _predict_media_type(url:str):
    TYPE_LOOKUP = {
        ".mp4":"video",
        ".webm":"video",
        ".png":"image",
        ".jpg":"image",
        ".jpeg":"image",
        ".gif":"animation",
    }
    _,ext = os.path.splitext(url)
    media_type = TYPE_LOOKUP[ext]
    return media_type


def _extract_images_from_html(html:str) -> list[str]:
    soup = bs4.BeautifulSoup(html,'html.parser')

    links = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            links.append(src)
    return links