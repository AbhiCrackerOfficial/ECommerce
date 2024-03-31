from django import template
from store.models import OrderItem
from django.db.models import Sum,F,FloatField
register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def divide(value, arg):
    try:
        return value / arg
    except ZeroDivisionError:
        return None
    
@register.filter
def order_total_amount(order):
    total_amount = order.orderitem_set.aggregate(total_price=Sum(F('quantity') * F('product__price'), output_field=FloatField()))['total_price'] or 0
    if total_amount:
        return total_amount
    return 0