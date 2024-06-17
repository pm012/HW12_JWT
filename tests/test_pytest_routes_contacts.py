from datetime import datetime
import os
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from src.services.auth import auth_service

# hw_path: str = str(Path(__file__).resolve().parent.parent.joinpath("hw14"))
# os.environ["PATH"] += os.pathsep + hw_path
# os.environ["PYTHONPATH"] += os.pathsep + hw_path

from src.database.models import User

# @patch("src.database.db.redis_pool", False)
def test_create_contact(client, contact, get_token):
    with patch.object(auth_service, 'cache') as r_mock:
        r_mock.get.return_value = None
        response = client.post("/api/contacts", json=contact, headers={"Authorization": get_token})
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == contact.get("first_name")
        assert "id" in data


# # @patch("src.database.db.redis_pool", False)
# def test_get_contact(client, token, contact):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.get("/api/contacts/1", headers={"Authorization": token})
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["first_name"] == contact.get("first_name")
#     assert "id" in data


# # @patch("src.database.db.redis_pool", False)
# def test_get_contact_not_found(client, token):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.get("/api/contacts/2", headers={"Authorization": token})
#     assert response.status_code == 404, response.text
#     data = response.json()
#     assert data["detail"] == "Not found"


# # @patch("src.database.db.redis_pool", False)
# def test_get_contacts(client, contact, token):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.get("/api/contacts", headers={"Authorization": token})
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert isinstance(data, list)
#     assert data[0]["first_name"] == contact.get("first_name")
#     assert "id" in data[0]


# # @patch("src.database.db.redis_pool", False)
# def test_update_contact(client, token):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.put("/api/contacts/1", json={"email": "new@email.com"}, headers={"Authorization": token})
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["email"] == "new@email.com"
#     assert "id" in data


# # @patch("src.database.db.redis_pool", False)
# def test_update_contact_not_found(client, token):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.put("/api/contacts/2", json={"email": "new@email.com"}, headers={"Authorization": token})
#     assert response.status_code == 404, response.text
#     data = response.json()
#     assert data["detail"] == "Not found"


# # @patch("src.database.db.redis_pool", False)
# def test_delete_contact(client, token):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.delete("/api/contacts/1", headers={"Authorization": token})
#     assert response.status_code == 204, response.text


# # @patch("src.database.db.redis_pool", False)
# def test_repeat_delete_contact(client, token):
#     # with patch("src.database.db.redis_pool", False):
#     response = client.delete("/api/contacts/1", headers={"Authorization": token})
#     assert response.status_code == 404, response.text
#     data = response.json()
#     assert data["detail"] == "Not found"