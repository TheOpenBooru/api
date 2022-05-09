
def update(name:str,namespace:str|None=None):
    tag = get(name)
    tag.namespace = namespace or tag.namespace
