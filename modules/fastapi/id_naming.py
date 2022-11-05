from fastapi.routing import APIRoute

def generate_unique_id(route: APIRoute):
    dirs = route.path.split("/")
    if len(dirs) == 1:
        return "index"
    else:
        return "_".join(dirs[1:])
