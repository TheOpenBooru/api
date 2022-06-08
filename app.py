from modules import database, logging, settings, importer
from endpoints import router

import uvicorn
from fastapi import FastAPI,responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(
    title="Open Booru",
    version="Alpha",
    docs_url='/docs',
)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_middleware(GZipMiddleware)


app.include_router(router)

@app.on_event("startup")
async def startup_event():
    if settings.IMPORT_LOCAL_ENABLED:
        await importer.import_files()
    if settings.IMPORT_SAFEBOORU_ENABLED:
        await importer.import_safebooru_search()
    database.Tag.regenerate()

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
        debug=True,
        host='0.0.0.0',
        port=settings.PORT,
        **ssl_params
    )