from rest_framework import generics
from payments.models import Payment
from .serializers import ReviewSerializer
# Create your views here.
class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET: List all payments.
    POST: Create a new payment.
    """
    queryset = Payment.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a payment.
    PUT/PATCH: Update a payment.
    DELETE: Delete a payment.
    """
    queryset = Payment.objects.all()
    serializer_class = ReviewSerializer
