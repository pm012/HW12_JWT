import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from httpx import AsyncClient
from main import app  # Assuming your FastAPI app instance is named 'app' in main.py
from src.schemas import UserDb

from src.database.db import get_db
from src.services.auth import auth_service
from src.repository import users as repository_users


from fastapi import Depends
from fastapi.testclient import TestClient

# Custom dependency override function
def override_get_current_user():
    return current_user

app.dependency_overrides[auth_service.get_current_user] = override_get_current_user

# Now the test will use the overridden dependency
@pytest.mark.asyncio
async def test_read_users_me(client, current_user):
    response = client.get("/api/users/me/")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == current_user.email
    assert data["username"] == current_user.username

# Remove the override after tests
app.dependency_overrides.pop(auth_service.get_current_user, None)

# Test for read_users_me endpoint
# @pytest.mark.asyncio
# async def test_read_users_me(client, current_user):
   
#     with patch.object(auth_service, 'get_current_user', return_value=current_user):
#         response = client.get("/api/users/me/")
#         assert response.status_code == 200
#         data = response.json()
#         assert data["email"] == current_user.email
#         assert data["username"] == current_user.username

# Test for update_avatar_user endpoint
# @pytest.mark.asyncio
# async def test_update_avatar_user(current_user, db, client):
#     file = MagicMock()
#     file.file = MagicMock()
    
#     # Mock cloudinary uploader response
#     upload_response = {
#         'version': '12345',
#         'public_id': f'ContactsApp/{current_user.username}'
#     }

#     with patch.object(auth_service, 'get_current_user', return_value=current_user):
#         with patch('cloudinary.uploader.upload', return_value=upload_response):
#             with patch('src.repository.users.update_avatar', return_value=UserDb(email=current_user.email, username=current_user.username, avatar="some_url")):
#                 response = await client.patch("/users/avatar", files={"file": ("filename", file.file, "image/jpeg")})
#                 assert response.status_code == 200
#                 data = response.json()
#                 assert data["email"] == current_user.email
#                 assert data["username"] == current_user.username
#                 assert "avatar" in data

if __name__ == "__main__":
    pytest.main()
