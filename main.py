import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis.asyncio as aioredis


from src.routes import contacts, auth, users
from src.conf.config import settings

origins = [ 
    "http://localhost:3000"
    ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)
    yield
    await redis.close()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def read_root():
    return {"message": "Hello World"}

