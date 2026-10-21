from rest_framework.pagination import PageNumberPagination


class TenantPagination(PageNumberPagination):
    """Custom pagination that respects tenant context."""
    page_size = 100
    max_page_size = 500
