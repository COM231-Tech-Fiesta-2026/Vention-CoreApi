from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager
from src.ventio_api.infrastructure.database.base_database import client


# Health check
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command("ping")
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

    yield

    client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    try:
        # Pings the database
        await client.admin.command("ping")
        return {"status": "online", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unreachable: {str(e)}")
