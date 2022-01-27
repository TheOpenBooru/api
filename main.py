import uvicorn
from endpoints import app

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=3000,debug=True)
