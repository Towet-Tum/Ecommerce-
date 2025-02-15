from rest_framework import serializers
from .models import Order, OrderItem, OrderShipment, ShippingMethod

# Updated OrderItemSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    # Instead of using a PrimaryKeyRelatedField referencing a ProductVariant model,
    # we simply accept a string that represents the external product variant ID.
    product_variant_id = serializers.CharField()

    class Meta:
        model = OrderItem
        # Assuming that the OrderItem model now has a field 'product_variant_id'
        # instead of a ForeignKey named "variant".
        fields = ['id', 'order', 'product_variant_id', 'quantity', 'unit_price', 'total_price']

    def validate(self, data):
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')
        total_price = data.get('total_price')
        if quantity is not None and unit_price is not None:
            expected_total = quantity * unit_price
            if total_price != expected_total:
                raise serializers.ValidationError("Total price must equal quantity multiplied by unit price.")
        return data


# Updated OrderSerializer
class OrderSerializer(serializers.ModelSerializer):
    # Instead of using a related Customer instance, we store a customer_id as a CharField.
    user_id = serializers.CharField()
    # Similarly, if shipping_address and billing_address come from another service,
    # store their external IDs as strings.
    shipping_address_id = serializers.CharField(required=False, allow_null=True)
    billing_address_id = serializers.CharField(required=False, allow_null=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        # Ensure these fields align with your updated Order model that uses external IDs.
        fields = [
            'id', 'user_id', 'order_date', 'status', 
            'shipping_address_id', 'billing_address_id', 'total_amount', 
            'tax_amount', 'shipping_cost', 'order_items'
        ]

    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Total amount cannot be negative.")
        return value


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'

class OrderShipmentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )
    shipping_method = ShippingMethodSerializer(read_only=True)
    shipping_method_id = serializers.PrimaryKeyRelatedField(
        queryset=ShippingMethod.objects.all(), source='shipping_method', write_only=True
    )
    
    class Meta:
        model = OrderShipment
        fields = [
            'id', 'order', 'order_id', 'shipping_method', 'shipping_method_id',
            'tracking_number', 'shipped_date', 'estimated_delivery_date'
        ]
