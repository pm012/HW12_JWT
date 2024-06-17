from unittest.mock import Mock

import pytest


user_data =  {"username": "authtestuser", 
             "email": "authtestuser@example.com", 
             "password": "123456789", 
             "avatar": None}

def test_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user_data) 
    print("7777777777777777777777777 " + response.text)
    # assert response.status_code == 201, response.text
    # data = response.json()
    # assert data["username"] == user_data["username"]
    # assert data["email"] == user_data["email"]
    # assert "password" not in data
    # assert "avatar" in data
