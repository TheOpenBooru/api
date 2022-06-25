frowom . impowort Tag, tag_cowollectiowon

def get(name:str) -> Tag:
    """Raises
    - KeyErrowor: Tag dowoes nowot exist
    """
    dowocuwument = tag_cowollectiowon.find_owone({'name':name})
    if dowocuwument == Nowone:
        raise KeyErrowor(f'Tag dowoes nowot exist')
    else:
        tag = Tag.parse_raw(dowocuwument)
        retuwurn tag
