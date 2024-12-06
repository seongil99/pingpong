from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20  # Default number of items per page
    limit_query_param = "limit"  # Query parameter name for limit
    offset_query_param = "offset"  # Query parameter name for offset
    max_limit = 100  # Maximum number of items a user can request


class StandardPagination(PageNumberPagination):
    page_size = 20  # Default number of items per page
    page_size_query_param = "page_size"  # Allows clients to specify the page size
    max_page_size = 100  # Maximum allowed page size
