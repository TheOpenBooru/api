import os
import uvicorn
from fastapi import FastAPI as _FastAPI
from endpoints import post,tag,file

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
app.include_router(tag.router,prefix="/images")

if __name__ == "__main__":
    uvicorn.run("app:app",host=os.getenv('HOSTNAME'), port=os.getenv('PORT'),debug=True)
