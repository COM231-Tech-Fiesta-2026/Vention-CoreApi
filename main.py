import uvicorn
from src.app import app
from fastapi.middleware.cors import CORSMiddleware

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0,0", port=8000, reload=True)
