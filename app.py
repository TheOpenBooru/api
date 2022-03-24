from modules import settings,importer
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
    allow_origins=["*"],allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


@app.get('/',tags=["Misc"])
def docs_redirect():
    return responses.RedirectResponse('/docs')

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await importer.import_files()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=settings.get('settings.site.port'),
        debug=True,
        # ssl_keyfile="./data/key.pem", 
        # ssl_certfile="./data/cert.pem",
    )