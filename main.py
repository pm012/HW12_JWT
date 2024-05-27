import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager


from src.routes import contacts, auth
from src.conf.config import settings

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@asynccontextmanager
async def lifespan():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

    yield

    # Shutdown logic (if any)
    await r.close()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

