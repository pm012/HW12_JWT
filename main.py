import os
from pathlib import Path
import redis.asyncio as aioredis
from fastapi import FastAPI, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from contextlib import asynccontextmanager
import redis.asyncio as aioredis


from src.routes import contacts, auth, users
from src.conf.config import settings
from src.database import db
from src.database.db import get_redis, redis_pool

origins = [ 
    "http://localhost:3000"
    ]

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     redis = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf8", decode_responses=True)
#     await FastAPILimiter.init(redis)
#     yield
#     await redis.close()

#app = FastAPI(lifespan=lifespan)
app = FastAPI()

# async def startup():
#     redis_live: bool | None = await db.check_redis()
#     if not redis_live:
#         # db.redis_pool = False
#         app.dependency_overrides[get_redis] = deny_get_redis
#     else:
#         await FastAPILimiter.init(get_redis())
#         app.dependency_overrides[get_limit] = RateLimiter(
#             times=settings.reate_limiter_times, seconds=settings.reate_limiter_seconds
#         )
@app.on_event("startup")
async def startup():
    r = await aioredis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        db=0,
        )
    await FastAPILimiter.init(r)

BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("src").joinpath("static")
app.mount("/static", StaticFiles(directory=directory), name="static")

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

# async def get_limit():
#     return None


# async def deny_get_redis():
#     return None

templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "our": "Build group WebPython #16"}
    )

