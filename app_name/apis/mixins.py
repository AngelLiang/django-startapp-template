from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    input_serializer_class = None
    output_serializer_class = None

    def get_input_serializer(self, *args, **kwargs):
        return self.input_serializer_class(*args, **kwargs)

    def get_output_serializer(self, *args, **kwargs):
        return self.output_serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return result_success()

    def perform_create(self, serializer):
        serializer.save()

    # def get_success_headers(self, data):
    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}


class ListModelMixin(object):
    """
    List a queryset.
    """

    output_serializer_class = None
    output_response_serializer_class = None

    def get_output_serializer(self, *args, **kwargs):
        return self.output_serializer_class(*args, **kwargs)

    def get_list_response(self, request, data, *args, **kwargs):
        # return Response(data, status=status.HTTP_200_OK)
        resp_data = OrderedDict([
            ('code', 0),
            ('data', data),
            ('errCode', ''),
            ('msg', ''),
        ])
        return Response(data=resp_data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    input_serializer_class = None
    output_serializer_class = None
    output_retrieve_serializer_class = None

    def get_input_serializer(self, *args, **kwargs):
        return self.input_serializer_class(*args, **kwargs)

    def get_output_serializer(self, *args, **kwargs):
        return self.output_serializer_class(*args, **kwargs)

    def get_output_retrieve_serializer(self, *args, **kwargs):
        if self.output_retrieve_serializer_class:
            return self.output_retrieve_serializer_class(*args, **kwargs)
        return self.output_serializer_class(*args, **kwargs)

    def retrieve(self, request, pk=None, **kwargs):
        """检索"""
        instance = self.get_object()
        serializer = self.get_output_retrieve_serializer(instance)
        # logger.debug(serializer.data)
        # return result_success(serializer.data)
        return Response(serializer.data)


class UpdateModelMixin(object):
    """
    更新
    """

    input_serializer_class = None
    output_serializer_class = None
    output_response_serializer_class = None

    def get_input_serializer(self, *args, **kwargs):
        return self.input_serializer_class(*args, **kwargs)

    def get_output_serializer(self, *args, **kwargs):
        return self.output_serializer_class(*args, **kwargs)

    def get_output_response_serializer(self, instance):
        if not self.output_response_serializer_class:
            raise ValueError('output_response_serializer_class had not set')
        kwargs = {
            'data': instance,
            'self': self.request.get_full_path()
        }
        return self.output_response_serializer_class(kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_input_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = self.get_output_serializer(instance)
        # self.serializer = self.get_output_response_serializer(instance)
        return Response(self.serializer.data, status=status.HTTP_200_OK)
        # return result_success(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """部分更新"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    删除
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
