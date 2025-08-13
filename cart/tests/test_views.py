import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@patch("cart.views.Product.objects.get")
@patch("cart.views.Cart.objects.get_or_create")
@patch("cart.views.CartItem.objects.get_or_create")
@pytest.mark.django_db
def test_add_to_cart_mocked(mock_get_or_create_cartitem, mock_get_or_create_cart, mock_product_get, api_client):
    user = User.objects.create_user(username="mockuser", password="testpass")
    api_client.force_authenticate(user=user)

    mock_product = MagicMock()
    mock_product_get.return_value = mock_product

    mock_cart = MagicMock()
    mock_get_or_create_cart.return_value = (mock_cart, True)

    mock_cart_item = MagicMock()
    mock_get_or_create_cartitem.return_value = (mock_cart_item, True)

    url = "/cart/add/1/"
    response = api_client.post(url)

    assert response.status_code == 200
    mock_product_get.assert_called_once_with(id=1)
    mock_get_or_create_cart.assert_called_once_with(user=user)
    mock_get_or_create_cartitem.assert_called_once_with(cart=mock_cart, product=mock_product)
