from django.urls import path 
from .views import CreatePayPalOrderView, CapturePayPalOrderView

urlpatterns = [
    # PayPal Payment Integration endpoints
    path('paypal/create/', CreatePayPalOrderView.as_view(), name='paypal-create'),
    path('paypal/capture/', CapturePayPalOrderView.as_view(), name='paypal-capture'),
]
