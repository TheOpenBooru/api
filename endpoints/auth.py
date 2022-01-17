from . import app
import logging
from typing import Any
from fastapi import Request,Query,APIRouter
from modules import captcha,auth,Validate
from modules.database import user

router = APIRouter()


@router.get('/captcha_sitekey')
# @app.state.limiter.limit("5/minute")
def get_sitekey() -> str:
    return captcha.SITEKEY

@router.post('/signup')
# @app.state.limiter.limt("2/minute")
def signup(username:str,password:str,email:str,g_captcha_response:str,req:Request) -> dict[str,Any]:
    if Validate.username(username):
        return {"success":False,"message":"Username does not fit criteria"}
    elif Validate.email(email):
        return {"success":False,"message":"Email is invalid"}
    elif user.search(name=username):
        return {"success":False,"message":"Username is already in use"}
    elif not captcha.verify(g_captcha_response) or user.search(email=email):
        # Send same response for email to prevent spam
        return {"success":False,"message":"Invalid Captcha Response"}
    else:
        uID = user.create(username,email)
        auth.user.create(uID,password)
        logging.info(f"User {uID} signed up on {req.client.host}")
        return {"success":True}

@router.post('/login')
# @app.state.limiter.limt("3/minute")
def login(email:str,password:str,g_captcha_response,req:Request):
    failed_message = {"success":False,"message":"Username or Password is incorrect"}
    try:
        user = user.get(email=email)
    except KeyError:
        return failed_message
    if auth.user.login(user['id'],password):
        return failed_message
    elif not captcha.verify(g_captcha_response):
        return failed_message
    else:
        jwt = auth.jwt.create(user['id'])
        return {"success":True,"token":jwt}
