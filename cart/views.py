from django.shortcuts import render, redirect
from .models import CartItem, Product
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            cart = request.user.cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return Response({'message': 'Product added to cart.'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = request.user.cart
        items = CartItem.objects.filter(cart=cart)
        cart_items = []
        total = 0
        for item in items:
            item_total = float(item.product.price) * item.quantity
            cart_items.append({
                'product': item.product.name,
                'price': float(item.product.price),
                'quantity': item.quantity,
                'total': item_total
            })
            total += item_total
        return Response({'items': cart_items, 'total': total}, status=status.HTTP_200_OK)