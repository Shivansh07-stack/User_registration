import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

# ------------------------------
# RegisterView Tests (mocking DB)
# ------------------------------
@patch("account.views.RegisterSerializer.save")
@patch("account.views.RegisterSerializer.is_valid", return_value=True)
@patch("account.views.RegisterSerializer.data", new_callable=lambda: {"username": "mockuser"})
def test_register_view_mock(mock_data, mock_is_valid, mock_save, api_client):
    mock_user = MagicMock(username="mockuser")
    mock_save.return_value = mock_user

    url = reverse("register")
    payload = {
        "username": "mockuser",
        "password": "pass123",
        "email": "mock@example.com",
        "mobile": "9999999999",
        "gender": "male",
        "address": "Test Address",
        "age": 25
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 200
    assert response.json()["msg"] == "User registered successfully"
    mock_save.assert_called_once()

# ------------------------------
# LoginView Tests (mock authenticate)
# ------------------------------
@patch("account.views.LoginSerializer.is_valid", return_value=True)
@patch("account.views.LoginSerializer.validated_data", new_callable=lambda: MagicMock())
@patch("account.views.RefreshToken.for_user")
def test_login_view_mock(mock_refresh_token, mock_validated_data, mock_is_valid, api_client):
    fake_token = MagicMock()
    fake_token.access_token = "access123"
    mock_refresh_token.return_value = fake_token

    url = reverse("login")
    payload = {"username": "mockuser", "password": "pass123"}
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 200
    mock_refresh_token.assert_called_once()

# ------------------------------
# EditUserView Tests (mock serializer)
# ------------------------------
@patch("account.views.UserSerializer.save")
@patch("account.views.UserSerializer.is_valid", return_value=True)
def test_edit_user_view_mock(mock_is_valid, mock_save, api_client):
    mock_user = MagicMock()
    api_client.force_authenticate(user=mock_user)

    url = reverse("edit")
    payload = {"first_name": "Updated"}
    response = api_client.put(url, payload, format="json")

    assert response.status_code == 200
    assert response.json()["msg"] == "Profile updated"
    mock_save.assert_called_once()

# ------------------------------
# LogoutView Tests (mock token delete)
# ------------------------------
def test_logout_view_mock(api_client):
    mock_user = MagicMock()
    mock_user.auth_token.delete = MagicMock()

    api_client.force_authenticate(user=mock_user)
    url = reverse("logout")
    response = api_client.post(url)

    assert response.status_code == 200
    assert response.json()["msg"] == "Logged out successfully"
    mock_user.auth_token.delete.assert_called_once()
