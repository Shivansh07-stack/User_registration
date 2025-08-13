# cart/views.py
from .models import Cart, CartItem, Product
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
            # Corrected: Get or create the cart for the user
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return Response({'message': 'Product added to cart.'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Corrected: Get the user's cart
            cart = Cart.objects.get(user=request.user)
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
            return Response({'items': cart_items, 'total': total})
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        

class CartDiscountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,dis):
        if dis < 0 or dis > 100:
            return Response({'error': 'Invalid discount percentage.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Corrected: Get the user's cart
            cart = Cart.objects.get(user=request.user)
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
                
            discount = dis*total/100
            total_amount = total-discount    
            return Response({'items': cart_items, 'total': total,'discount_percentage': str(dis)+"%","discount": discount, "total_after_discount": total_amount})
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            cart_item = CartItem.objects.get(id=product_id, cart__user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)