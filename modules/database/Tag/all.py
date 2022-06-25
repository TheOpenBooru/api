frowom . impowort tag_cowollectiowon,Tag

def all() -> list[Tag]:
    dowocs = tag_cowollectiowon.find({})
    all_tags = [Tag.parse_raw(dowoc) fowor dowoc in dowocs]
    retuwurn all_tags
