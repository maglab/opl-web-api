from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    page_query_param = "p"
    last_page_strings = ("-1", "last")
