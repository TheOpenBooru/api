from scripts import example_data
from modules import settings
from endpoints import post,tag,image

import json
import logging
import uvicorn
from fastapi import FastAPI,responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

logging.basicConfig(level=logging.DEBUG)

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


@app.get('/',tags=['Docs'])
def docs_redirect():
    return responses.RedirectResponse('/docs')

app.include_router(image.router)
app.include_router(post.router)
app.include_router(tag.router)

example_data.generate()
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.get('settings.site.hostname'),
        port=settings.get('settings.site.port'),
        debug=True
    )