from fastapi import FastAPI, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.ventio_api.infrastructure.database.base_database import client
from fastapi.middleware.cors import CORSMiddleware
from src.ventio_api.api.routes import auth_routes, user_routes, conversation_route


# Health check
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command("ping")
        print("MongoDB connected successfully!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

    yield

    client.close()


app = FastAPI(lifespan=lifespan)

router = APIRouter(prefix="/api/v1")

router.include_router(auth_routes.router)
router.include_router(user_routes.router)
router.include_router(conversation_route.router)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    try:
        # Pings the database
        await client.admin.command("ping")
        return {"status": "online", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unreachable: {str(e)}")
