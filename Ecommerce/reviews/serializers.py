from rest_framework import serializers
from catalog.models import Product 
from . models import Review
from users.models import CustomUser
from catalog.serializers import ProductSerializer
from users.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model



class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    customer = CustomUserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='customer', write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'product_id', 'customer', 'customer_id', 'rating', 'review_text', 'review_date']
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")