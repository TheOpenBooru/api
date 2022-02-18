from scripts import example_data
from modules import settings
from endpoints import post,tag
from endpoints.dependencies import auth

import logging
import uvicorn
from fastapi import FastAPI,responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
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
app.add_middleware(GZipMiddleware)


app.add_exception_handler(auth.jwt.BadTokenError,auth.bad_token_exception_handler)

@app.get('/',tags=["Unprivileged"])
def docs_redirect():
    return responses.RedirectResponse('/docs')

app.include_router(post.router)
app.include_router(tag.router)

if __name__ == "__main__":
    example_data.generate()
    uvicorn.run(
        "app:app",
        host=settings.get('settings.site.hostname'),
        port=settings.get('settings.site.port'),
        debug=True
    )