from scripts import example_data
from modules import settings
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


@app.get('/',tags=['Docs'])
def docs_redirect():
    return responses.RedirectResponse('/docs')

app.include_router(router)

example_data.generate(50)
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=settings.get('settings.site.port'),
        debug=True
    )