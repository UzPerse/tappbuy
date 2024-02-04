from django_filters.rest_framework import FilterSet
from .models import *


# Product Filter Class
class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category_id': ['in', 'exact'],
        }


# Product Variant Filter
class ProductVariantFilter(FilterSet):
    class Meta:
        model = ProductVariant
        fields = {
            'product__category_id': ['in', 'exact'],
        }
