from rest_framework.pagination import PageNumberPagination


class KgPagination:

    @staticmethod
    def get_page_size(limit):
        paginator = PageNumberPagination()
        if limit and int(limit) >= 1:
            return limit
        return paginator.page_size

    @staticmethod
    def get_response(limit, items, request, Serializer):
        paginator = PageNumberPagination()
        paginator.page_size = int(limit) if limit and int(limit) >= 1 else paginator.page_size
        result_page = paginator.paginate_queryset(items, request)
        serializer = Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
