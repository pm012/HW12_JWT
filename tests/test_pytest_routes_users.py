import pytest
from unittest.mock import MagicMock, patch
from fastapi import Depends
from starlette.datastructures import UploadFile

# Test for read_users_me endpoint
@pytest.mark.asyncio
async def test_read_users_me(client, user, token):
   
    response = client.get("/api/users/me/", headers={"Authorization": token})        
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.get("email")
    assert data["username"] == user.get("username")

# Test for update_avatar_user endpoint
#@pytest.mark.asyncio
# async def test_update_avatar_user(user, client, session, token):
#     file = MagicMock()
#     file.read.return_value = b"fake_image_data"
    
#     with patch("starlette.datastructures.UploadFile", return_value=file):
#         response = client.patch("/api/users/avatar", 
#                             headers={"Authorization": token},
#                             files={"file": ("filename.jpeg", file.read(), "image/jpeg")}
#                             )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["email"] == user.get("email")
#     assert data["username"] == user.get("username")
#     assert "avatar" in data



# Test for update_avatar_user endpoint
@pytest.mark.asyncio
async def test_update_avatar_user(user, client, session, token):
    # Mock file content and metadata
    file_content = b"fake_image_data"
    upload_file = UploadFile(filename="filename.jpeg", file=MagicMock())
    upload_file.file.read.return_value = file_content

    # Make the patch request with the mock file
    response = client.patch(
        "/api/users/avatar",
        headers={"Authorization": token},
        files={"file": ("filename.jpeg", file_content, "image/jpeg")}
    )

    # Check response status and content
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.get("email")
    assert data["username"] == user.get("username")
    assert "avatar" in data


if __name__ == "__main__":
    pytest.main()
