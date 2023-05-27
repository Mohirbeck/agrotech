from django_filters import rest_framework as filters
from .models import (
    Cart,
    Product,
    Order,
)

class CartFilter(filters.FilterSet):
    class Meta:
        model = Cart
        fields = {
            "user": ["exact"],
            "product": ["exact"],
            "quantity": ["exact", "lt", "gt"],
            "created_at": ["exact", "lt", "gt"],
            "updated_at": ["exact", "lt", "gt"],
        }

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "icontains"],
            "category": ["exact"],
            "description": ["exact", "icontains"],
            "created_at": ["exact", "lt", "gt"],
            "updated_at": ["exact", "lt", "gt"],
        }

class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            "user": ["exact"],
            "status": ["exact"],
            "payment_status": ["exact"],
            "created_at": ["exact", "lt", "gt"],
            "updated_at": ["exact", "lt", "gt"],
        }