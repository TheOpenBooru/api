from fastapi.routing import APIRoute

def generate_unique_id(route: APIRoute):
    return route.name
