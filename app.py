import uvicorn
from fastapi import FastAPI as _FastAPI
from endpoints import auth,post,tag

import dotenv
dotenv.load_dotenv()

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s; %(name)s; %(levelname)s; %(message)s',
    filename='/tmp/OpenBooru.log',
    filemode='a',
)

app = _FastAPI()

app.include_router(auth.router,prefix="/v1/auth")
app.include_router(post.router,prefix="/v1/post")
app.include_router(tag.router,prefix="/v1/tag")

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=57255,debug=True)
