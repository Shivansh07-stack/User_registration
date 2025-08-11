from django.urls import path
from .views import AddToCartView, CartDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view()),
    path('cart/', CartDetailView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]