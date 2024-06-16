from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

import redis.asyncio as redis
import logging

logger = logging.getLogger(f"users.{__name__}")

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
#environ.Env.read_env(BASE_DIR / '.env')

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_redis():
    return redis.ConnectionPool(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        # password=settings.redis_password,
        db=0,
        decode_responses=False,
    )


def get_redis() -> redis.Redis | None:
    # Here, we re-use our connection pool
    # not creating a new one
    try:
        logger.debug("get_redis connection_pool")
        if redis_pool:
            connection = redis.Redis(connection_pool=redis_pool)
            return connection
        logger.debug("get_redis connection_pool None")
    except:
        logger.debug("get_redis except")


async def check_redis() -> bool | None:
    try:
        logger.debug("check_redis")
        r: redis.Redis | None = get_redis()
        if r:
            return await r.ping()
    except Exception:
        logger.debug("check_redis fail")
        return None


redis_pool: redis.ConnectionPool = create_redis()