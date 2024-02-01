from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.utils.urls import replace_query_param, remove_query_param


# Pagination function
class ProductPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'current_page': self.page.number,
            'per_page': self.page_size,
            'total_pages': self.page.paginator.num_pages,
            'results': data,

        })
