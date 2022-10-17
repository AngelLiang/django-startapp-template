from collections import OrderedDict
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework import status


def get_paginated_data(pagination_class, serializer_class, queryset, request, view):
    """获取分页数据"""
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return serializer.data


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    """获取分页响应"""
    data = get_paginated_data(pagination_class, serializer_class, queryset, request, view)
    # return Response(data=data, status=status.HTTP_200_OK)
    resp_data = OrderedDict([
        ('code', 0),
        ('data', data),
        ('errCode', ''),
        ('msg', ''),
    ])
    return Response(data=resp_data)


class CustomPageNumberPagination(PageNumberPagination):

    page_query_param = 'current'
    page_query_description = '当前页面'
    page_size_query_param = 'size'
    page_size_query_description = '每页大小'
    max_page_size = 1000

    def __init__(self, pagesize=None):
        self.page_size = pagesize

    def get_paginated_response(self, data):
        if not getattr(self, 'page', None):
            page_query_param = self.request.query_params.get(self.page_query_param, 0)
            page_size_query_param = self.request.query_params.get(self.page_size_query_param, 0)
            r_data = {
                self.page_query_param: page_query_param,
                self.page_size_query_param: page_size_query_param,
                'total': len(data),
                # 'page': page_query_param,
                'records': data,
            }
        else:
            r_data = {
                self.page_query_param: self.page.number,
                self.page_size_query_param: self.page.paginator.per_page,
                'total': self.page.paginator.count,
                'page': self.page.paginator.num_pages,
                'records': data,
            }
        # r_data = {
        #     self.page_query_param: self.page.number,
        #     self.page_size_query_param: self.page.paginator.per_page,
        #     'total': self.page.paginator.count,
        #     'page': self.page.paginator.num_pages,
        #     'records': data,
        # }

        resp_data = OrderedDict([
            ('code', 0),
            ('data', r_data),
            ('errCode', ''),
            ('msg', ''),
        ])
        # serializer = PaginationOuputSerializer(resp_data)
        return Response(data=resp_data)

    def get_results(self, data):
        return data['data']

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        self.paginator = paginator
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            # msg = self.invalid_page_message.format(
            #     page_number=page_number, message=str(exc)
            # )
            # raise NotFound(msg)
            return []

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        return list(self.page)
