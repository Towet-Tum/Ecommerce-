import logging

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)

class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET: List all orders for the authenticated user.
    POST: Create a new order.
    
    Note: In a microservices architecture, the order model stores external IDs (e.g. customer_id)
    instead of direct ForeignKey relationships.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter orders to only include those for the authenticated user,
        # using the external user identifier.
        return Order.objects.filter(user_id=str(self.request.user.id))
    
    def perform_create(self, serializer):
        # Save the order with the external user_id from the authenticated user.
        order = serializer.save(user_id=str(self.request.user.id))
        # Optionally, offload order total calculation or other business logic asynchronously.
        try:
            from .tasks import update_order_totals
            update_order_totals.delay(order.id)
        except ImportError as e:
            logger.warning("Asynchronous task 'update_order_totals' not available: %s", e)
        return order


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve an order.
    PUT/PATCH: Update an order.
    DELETE: Delete an order.
    
    Only orders belonging to the authenticated user are accessible.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure that only orders for the authenticated user's external user_id are returned.
        return Order.objects.filter(user_id=str(self.request.user.id))
