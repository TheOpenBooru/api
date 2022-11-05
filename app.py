from modules import settings, daemon
from modules.fastapi import main_router
from modules.fastapi.middleware import middlewares
import uvicorn
from fastapi import FastAPI, responses
from fastapi.routing import APIRoute

def custom_generate_unique_id(route: APIRoute):
    dirs = route.path.split("/")
    if len(dirs) == 1:
        return "index"
    else:
        return "_".join(dirs[1:])

app = FastAPI(
    title="Open Booru",
    version="Lithium", 
    docs_url='/docs',
    middleware=middlewares,
    generate_unique_id_function=custom_generate_unique_id,
    responses={
        200: {"description":"Success"},
        401: {"description":"Account Required"},
        403: {"description":"Missing Permission"},
        429: {"description":"Rate limitted"},
    },
)
app.include_router(main_router)


@app.on_event("startup")
async def startup_event():
    daemon.run_daemon()


@app.get('/',include_in_schema=False)
def docs_redirect():
    return responses.RedirectResponse('/docs')


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=settings.PORT,
        log_config="./data/logging.conf",
        ssl_keyfile=settings.SSL_KEY_STORE if settings.SSL_ENABLED else None,
        ssl_certfile=settings.SSL_CERT_STORE if settings.SSL_ENABLED else None,
    )
