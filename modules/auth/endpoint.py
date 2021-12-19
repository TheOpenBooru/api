from modules import auth,database
import fastapi

LOGIN_SUCCESS = lambda t:fastapi.Response({
    "success":True,
    "message":"Signin Successful",
    "token":t
    },200)
LOGIN_FAILURE = lambda:fastapi.Response({
    "success":False,
    "message":"Invalid username or password"
    },404)


@app.get("/auth/login")
def login(email:str,password:str):
    try:
        user = database._user.search(email=email)
    except KeyError:
        return LOGIN_FAILURE()
    else:
        token = auth.login(user,password)
        if token:
            return LOGIN_SUCCESS(token)
        else:
            return LOGIN_FAILURE()

@app.get("/auth/register")
def register(name:str,email:str,password:str):
    try:
        user = User.get()
    except Exception as e:
        print(e)