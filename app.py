import uvicorn
from fastapi import FastAPI as _FastAPI
from endpoints import post,tag



import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s; %(name)s; %(levelname)s; %(message)s',
    filename='/tmp/OpenBooru.log',
    filemode='a',
)

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

app.include_router(post.router,prefix="/post")
app.include_router(tag.router,prefix="/tag")

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0", port=57255,debug=True)
