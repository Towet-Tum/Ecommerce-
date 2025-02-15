from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, OrderShipment

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'order_date', 'status', 'total_amount')
    list_filter = ('status', 'order_date')
    search_fields = ('user__email',)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant_id', 'quantity', 'total_price')
    list_filter = ('order', 'product_variant_id')
    
    
@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_cost')
    search_fields = ('name',)

@admin.register(OrderShipment)
class OrderShipmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'shipping_method', 'tracking_number', 'shipped_date')
    list_filter = ('shipped_date', 'shipping_method')
    search_fields = ('order__id', 'tracking_number')
