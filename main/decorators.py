from functools import wraps
from copy import copy

from rest_framework.response import Response
from django.http import HttpResponseRedirect

from .exceptions import UrlSpaceExhaust, NeedPassword, BadParams, UrlHasBeenUsed


def _short_url_exception_decorator(exception, res):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except exception as e:
                return res(e)
            else:
                return result

        return inner

    return decorator


def need_password_view_res(e):
    return HttpResponseRedirect('/check?short_url=' + e.args[0])


protect_url_space_exhaust = _short_url_exception_decorator(UrlSpaceExhaust, lambda e: Response(
    UrlSpaceExhaust.content,
    UrlSpaceExhaust.api_status
))

protect_url_has_been_used = _short_url_exception_decorator(UrlHasBeenUsed, lambda e: Response(
    UrlHasBeenUsed.content,
    UrlHasBeenUsed.api_status
))

url_need_password_with_api = _short_url_exception_decorator(NeedPassword, lambda e: Response(
    NeedPassword.content,
    NeedPassword.api_status
))

url_need_password_with_view = _short_url_exception_decorator(NeedPassword, need_password_view_res)


def api_data_validate(serializer, inBody=True):
    def decorator(func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            data = request.data if inBody else request.query_params
            serializer_data = serializer(data=data)
            if serializer_data.is_valid():
                request.validate_data = serializer_data.data
                return func(self, request, *args, **kwargs)
            else:
                content = copy(BadParams.content)
                content.update(serializer_data.errors)
                return Response(
                    content,
                    status=BadParams.api_status
                )

        return inner

    return decorator
