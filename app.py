from modules import settings
from endpoints import post,tag

import os
import uvicorn
from fastapi import FastAPI as _FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = _FastAPI(
    version="Alpha",
    docs_url='/docs',
    openapi_tags=[
        {
            "name":"Unprivileged",
            "description":"These endpoints can be accessed without an account"}
        ]
    )

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"],
)

@app.get('/',tags=["Unprivileged"])
def docs_redirect():
    return RedirectResponse('/docs')


app.include_router(post.router,prefix="/posts",tags=["Post"])
app.include_router(tag.router,prefix="/tags",tags=["Tag"])

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.get('settings.site.hostname'),
        port=settings.get('settings.site.port'),
        debug=True
    )