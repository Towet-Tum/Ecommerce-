import base64
import requests

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



# Import models and serializers
from .models import Payment
from .serializers import PaymentSerializer

# Create your views here.

# --- Payments ---
class PaymentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all payments.
    POST: Create a new payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a payment.
    PUT/PATCH: Update a payment.
    DELETE: Delete a payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]




# ===============================================================
# Section 2: PayPal Payment Integration Endpoints
# ===============================================================
# Helper function to get the PayPal token
def get_paypal_token():
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_auth}",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

class CreatePayPalOrderView(APIView):
    """
    Create a PayPal order and return the order ID and approval URL.
    
    This endpoint accepts dynamic parameters via POST:
      - amount: Order amount (default "100.00")
      - currency_code: e.g. "USD" (default "USD")
      - reference_id: Unique reference ID (default "ORDER_REF_001")
      - description: Order description (default "Purchase from Your Store")
      - soft_descriptor: Descriptor for the transaction (default "YourDescriptor")
      - brand_name: Your brand name (default "Your Brand Name")
      - return_url: URL to redirect after approval (default built from /api/paypal/capture/)
      - cancel_url: URL to redirect if canceled (default built from /api/paypal/cancel/)
      - landing_page, shipping_preference, user_action: Optional additional parameters.
      
    If the user is authenticated and no custom_id is provided, the user's ID is used.
    """
    def post(self, request, *args, **kwargs):
        token = get_paypal_token()
        if not token:
            return Response({"error": "Unable to obtain PayPal token."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        
        # Retrieve dynamic parameters from request.data with defaults
        amount_value = request.data.get("amount", "100.00")
        currency_code = request.data.get("currency_code", "USD")
        reference_id = request.data.get("reference_id", "ORDER_REF_001")
        description = request.data.get("description", "Purchase from Your Store")
        soft_descriptor = request.data.get("soft_descriptor", "YourDescriptor")
        brand_name = request.data.get("brand_name", "Your Brand Name")
        return_url = request.data.get("return_url", request.build_absolute_uri("/api/paypal/capture/"))
        cancel_url = request.data.get("cancel_url", request.build_absolute_uri("/api/paypal/cancel/"))
        landing_page = request.data.get("landing_page", "BILLING")
        shipping_preference = request.data.get("shipping_preference", "NO_SHIPPING")
        user_action = request.data.get("user_action", "CONTINUE")
        
        # Use user ID as custom_id if authenticated, otherwise "guest" or overridden value.
        custom_id = str(request.user.id) if request.user.is_authenticated else request.data.get("custom_id", "guest")
        
        json_data = {
            "intent": "CAPTURE",
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url,
                "brand_name": brand_name,
                "landing_page": landing_page,
                "shipping_preference": shipping_preference,
                "user_action": user_action
            },
            "purchase_units": [
                {
                    "reference_id": reference_id,
                    "description": description,
                    "custom_id": custom_id,
                    "soft_descriptor": soft_descriptor,
                    "amount": {
                        "currency_code": currency_code,
                        "value": amount_value
                    }
                }
            ]
        }
        
        paypal_order_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        response_paypal = requests.post(paypal_order_url, json=json_data, headers=headers)
        
        if response_paypal.status_code in [200, 201]:
            data = response_paypal.json()
            # Extract the approval URL from the returned links.
            approval_url = next(
                (link.get("href") for link in data.get("links", []) if link.get("rel") == "approve"),
                None
            )
            return Response({"order_id": data.get("id"), "approval_url": approval_url},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": response_paypal.json()},
                            status=response_paypal.status_code)

class CapturePayPalOrderView(APIView):
    """
    Capture a PayPal order after the buyer approves the payment.
    Expects 'order_id' in the POST data.
    """
    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        if not order_id:
            return Response({"error": "order_id is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        token = get_paypal_token()
        if not token:
            return Response({"error": "Unable to obtain PayPal token."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
        response_paypal = requests.post(capture_url, headers=headers)
        
        if response_paypal.status_code in [200, 201]:
            capture_data = response_paypal.json()
            # Business logic: Update internal order status here if needed.
            return Response(capture_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": response_paypal.json()},
                            status=response_paypal.status_code)


class CapturePayPalOrderView(APIView):
    """
    Capture a PayPal order after the buyer approves the payment.
    Expects 'order_id' in the POST data.
    """
    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        if not order_id:
            return Response({"error": "order_id is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        token = get_paypal_token()
        if not token:
            return Response({"error": "Unable to obtain PayPal token."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
        response_paypal = requests.post(capture_url, headers=headers)
        
        if response_paypal.status_code in [200, 201]:
            capture_data = response_paypal.json()
            # Offload updating payment status and sending confirmation email
            from .tasks import update_payment_status, send_order_confirmation_email
            # Example: Assume you have a Payment instance associated with this order.
            # update_payment_status.delay(payment_id, 'completed')
            # And send order confirmation email
            send_order_confirmation_email.delay(order_id)
            return Response(capture_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": response_paypal.json()},
                            status=response_paypal.status_code)


############################################################
#The JSON code for testing the paypal/create endpoint
'''
    {
  "amount": "150.00",
  "currency_code": "USD",
  "reference_id": "ORDER_REF_002",
  "description": "Purchase from Your Store",
  "soft_descriptor": "YourDescriptor",
  "brand_name": "Your Brand Name",
  "return_url": "http://localhost:8000/api/paypal/capture/",
  "cancel_url": "http://localhost:8000/api/paypal/cancel/",
  "landing_page": "BILLING",
  "shipping_preference": "NO_SHIPPING",
  "user_action": "CONTINUE",
  "custom_id": "CUSTOMER_ID_OR_CUSTOM_VALUE"
}

'''