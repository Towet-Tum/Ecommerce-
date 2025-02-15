from rest_framework import serializers
from orders.serializers import OrderSerializer
from .models import Payment
from orders.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'payment_method', 'payment_date', 'amount', 'status']
    
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Payment amount cannot be negative.")
        return value
