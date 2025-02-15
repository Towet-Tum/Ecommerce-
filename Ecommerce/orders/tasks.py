from celery import shared_task
from .models import Order

@shared_task
def update_order_totals(order_id):
    """
    Recalculate and update the order total amount based on order items.
    """
    try:
        order = Order.objects.get(id=order_id)
        total = sum(item.total_price for item in order.order_items.all())
        order.total_amount = total
        order.save(update_fields=['total_amount'])
    except Order.DoesNotExist:
        # Log error if necessary
        pass
