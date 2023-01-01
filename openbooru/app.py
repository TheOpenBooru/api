from openbooru.modules import settings, daemon, database
from openbooru.modules.fastapi import main_router, initialise_fastapi_cache, generate_unique_id
from openbooru.modules.fastapi.middleware import middlewares
import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Open Booru",
    version="Lithium", 
    docs_url='/docs',
    middleware=middlewares,
    generate_unique_id_function=generate_unique_id,
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
    initialise_fastapi_cache()
    daemon.run_daemon()


def run():
    uvicorn.run(
        "openbooru:app",
        host='0.0.0.0',
        port=settings.PORT,
        log_config="./data/logging.conf",
        ssl_keyfile=settings.SSL_KEY_STORE if settings.SSL_ENABLED else None,
        ssl_certfile=settings.SSL_CERT_STORE if settings.SSL_ENABLED else None,
    )


if __name__ == "__main__":
    run()