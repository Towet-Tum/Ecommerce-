from django.urls import path 
from .views import OrderListCreateView, OrderDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
     # Orders endpoints
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
