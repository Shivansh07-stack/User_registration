import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
@patch("cart.views.Product.objects.get")
@patch("cart.views.Cart.objects.get_or_create")
@patch("cart.views.CartItem.objects.get_or_create")
def test_add_to_cart_mocked(mock_get_or_create_cartitem, mock_get_or_create_cart, mock_product_get):
    # Create fake user
    user = User.objects.create_user(username="mockuser", password="testpass")

    # Mock Product
    fake_product = MagicMock()
    fake_product.id = 1
    fake_product.name = "Mock Product"
    fake_product.price = 50
    mock_product_get.return_value = fake_product

    # Mock Cart
    fake_cart = MagicMock()
    mock_get_or_create_cart.return_value = (fake_cart, True)

    # Mock CartItem
    fake_cart_item = MagicMock(quantity=1)
    mock_get_or_create_cartitem.return_value = (fake_cart_item, True)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('add_to_cart', kwargs={'product_id': 1})
    response = client.post(url)

    assert response.status_code == 200
    assert response.json()['message'] == "Product added to cart"
    mock_product_get.assert_called_once_with(id=1)
    mock_get_or_create_cart.assert_called_once_with(user=user)
