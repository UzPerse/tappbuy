from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler
from django.core.paginator import Paginator
from .models import *
from .serializers import *
from .filters import *
from .pagination import *


# Store data API View
class StoreDetailView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializers


# Category API View
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Product API View
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('?')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['name', 'category__name', 'brand__name']

    def handle_exception(self, exc):
        queryset = Product.objects.all().order_by('?')
        pagination = Paginator(queryset, per_page=6)

        if isinstance(exc, NotFound):
            return Response({
                'next': None,
                'previous': None,
                'total': pagination.count,
                'per_page': self.pagination_class.page_size,
                'total_pages': pagination.num_pages,
                'results': [],
            })
        return super().handle_exception(exc)


# Product detail View
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Product Variant View
class ProductVariantListView(generics.ListAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
