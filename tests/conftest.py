import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User
from main import app
from src.database.models import Base
from src.database.db import get_db, get_redis
from unittest.mock import MagicMock, patch, AsyncMock


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def mock_ratelimiter(monkeypatch):
    mock_rate_limiter = AsyncMock()
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", mock_rate_limiter)
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", mock_rate_limiter)
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", mock_rate_limiter)


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    async def override_get_limit():
        return None

    async def override_get_redis():
        return None        

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
     return {"username": "testuser", 
             "email": "testuser@example.com", 
             "password": "123456789", 
             "avatar": None}


def create_user(client, session, user, monkeypatch):

    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.email.send_email", mock_send_email)

    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()

    mock_avatar = AsyncMock(spec=User)
    mock_avatar.username = current_user.username
    mock_avatar.email = current_user.email
    mock_avatar.avatar = "test.jpeg"
    monkeypatch.setattr("src.repository.users.update_avatar", mock_avatar)

    upload_response = {
        'version': '12345',
        'public_id': f'ContactsApp/{user.get("username")}'
    }

    mock_cloudinary = MagicMock(upload_response)
    monkeypatch.setattr("cloudinary.uploader.upload", mock_cloudinary)

def get_access_token_user(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    
    data = response.json()
    access_token = data["access_token"]
    return f"Bearer {access_token}"


@pytest.fixture()
def token(client, user, session, monkeypatch):
    """ get auth token foa all auth requests
        mock_ratelimiter not used, but required in argumants for execute fixture before
    """
    create_user(client, session, user, monkeypatch)
    
    return get_access_token_user(client, user)

