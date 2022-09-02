from modules import settings, importers, tags
from modules.fastapi import main_router
from modules.fastapi.middleware import middlewares

import uvicorn
from fastapi import FastAPI,responses

app = FastAPI(
    title="Open Booru",
    version="Alpha", 
    docs_url='/docs',
    middleware=middlewares,
)
app.include_router(main_router)


@app.on_event("startup")
async def startup_event():
    await importers.import_all()
    if settings.TAGS_REGENERATE_ON_BOOT:
        try:
            tags.regenerate()
        except KeyboardInterrupt:
            print("Manually Skippped Tag Regenerated")


@app.get('/',include_in_schema=False)
def docs_redirect():
    return responses.RedirectResponse('/docs')


ssl_params = {}
if settings.SSL_ENABLED:
    ssl_params |= {
        "ssl_keyfile":settings.SSL_KEY_STORE,
        "ssl_certfile":settings.SSL_CERT_STORE,
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=settings.PORT,
        log_config="./data/logging.conf",
        **ssl_params,
    )
