import uvicorn
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(debug=True)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from endpoints import auth

@app.get('/auth/captcha_sitekey')
@limiter.limit("5/minute")
def get_sitekey(request):
    return auth.get_sitekey()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, log_level="info",debug=True)
