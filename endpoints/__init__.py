from fastapi import FastAPI as _FastAPI
app = _FastAPI(debug=True)

from . import auth,post,tag
app.include_router(auth.router,prefix="/v1/auth")
app.include_router(post.router,prefix="/v1/post")
app.include_router(tag.router,prefix="/v1/tag")