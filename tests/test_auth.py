import pytest
from jose import jwt
from main import SECRET_KEY, ALGORITHM

def test_create_user(client):
    response = client.post("/users/create", json={
        "email": "user@example.com",
        "password": "password123",
        "name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "id" in data

def test_create_user_duplicate_email(client, test_user):
    response = client.post("/users/create", json={
        "email": test_user["email"],
        "password": "password123",
        "name": "Another User"
    })
    assert response.status_code == 400

def test_login_user(client, test_user):
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 403

def test_login_nonexistent_user(client):
    response = client.post("/login", data={
        "username": "nonexistent@example.com",
        "password": "password123"
    })
    assert response.status_code == 403 