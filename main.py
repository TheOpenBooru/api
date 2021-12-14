# from endpoints import .

import fastapi
import uvicorn

app = fastapi.FastAPI()

@app.get("/")
def root():
    return fastapi.responses.RedirectResponse('/openapi.json')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, log_level="info",debug=True)
