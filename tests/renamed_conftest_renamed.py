import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

#from fastapi_limiter.depends import RateLimiter
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from src.database.models import User

from main import app
from src.services.auth import auth_service
from src.database.models import Base
from src.database.db import get_db, get_redis

#from unittest.mock import MagicMock, patch, AsyncMock


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine) 

test_user = {"username": "testuser", 
             "email": "testuser@example.com", 
             "password": "123456789", 
             "avatar": None}

@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal as session:
            hash_password = auth_service.get_password_hash(test_user["password"])
            current_user = User(username=test_user["username"], email=test_user["email"], password=hash_password, confirmed=True)
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())

# @pytest.fixture(scope="module")
# def session():
#     # Create the database

#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture()
# def mock_ratelimiter(monkeypatch):
#     mock_rate_limiter = AsyncMock()
#     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", mock_rate_limiter)
#     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", mock_rate_limiter)
#     monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", mock_rate_limiter)


@pytest.fixture(scope="module")
def client():
    # Dependency override

    async def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        except Exception as e:
            print(e)
            await session.rollback()
        finally:
            await session.close()

    # async def override_get_limit():
    #     return None

    # async def override_get_redis():
    #     return None        

    app.dependency_overrides[get_db] = override_get_db
    # app.dependency_overrides[get_redis] = override_get_redis

    yield TestClient(app)


# @pytest.fixture(scope="module")
# def user():
#      return {"username": "testuser", 
#              "email": "testuser@example.com", 
#              "password": "123456789", 
#              "avatar": None}


# def create_user(client, session, user, monkeypatch):

#     mock_send_email = MagicMock()
#     monkeypatch.setattr("src.services.email.send_email", mock_send_email)

#     response = client.post(
#         "/api/auth/signup",
#         json=user,
#     )
#     current_user: User = session.query(User).filter(User.email == user.get("email")).first()
#     current_user.confirmed = True
#     session.commit()

#     mock_avatar = AsyncMock(spec=User)
#     mock_avatar.username = current_user.username
#     mock_avatar.email = current_user.email
#     mock_avatar.avatar = "test.jpeg"
#     monkeypatch.setattr("src.repository.users.update_avatar", mock_avatar)

#     upload_response = {
#         'version': '12345',
#         'public_id': f'ContactsApp/{user.get("username")}'
#     }

#     mock_cloudinary = MagicMock(upload_response)
#     monkeypatch.setattr("cloudinary.uploader.upload", mock_cloudinary)

# def get_access_token_user(client, user):
#     response = client.post(
#         "/api/auth/login",
#         data={"username": user.get("email"), "password": user.get("password")},
#     )
    
#     data = response.json()
#     access_token = data["access_token"]
#     return f"Bearer {access_token}"


# @pytest.fixture()
# def token(client, user, session, monkeypatch):
#     """ get auth token foa all auth requests
#         mock_ratelimiter not used, but required in argumants for execute fixture before
#     """
#     create_user(client, session, user, monkeypatch)
    
#     return get_access_token_user(client, user)

# @pytest.fixture(scope="module")
# def contact():
#     result = {
#         "first_name": "aaaa",
#         "last_name": "bbbbb",
#         "email": "aaa@uu.cc",
#         "phone": None,
#         "birthday": None,
#         "comments": None,
#         "favorite": False,
#         "user_id": 1,
#     }
#     return result

