from functools import wraps

from rest_framework.response import Response
from django.http import JsonResponse

from .exceptions import UrlSpaceExhaust, NeedPassword, BadParams, UrlHasBeenUsed


def _short_url_exception_decorator(exception, res):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except exception:
                return res()
            else:
                return result

        return inner

    return decorator


def need_password_view_res():
    # todo:应该重定向输入密码的页面
    res = JsonResponse(
        NeedPassword.content,
    )
    res.status_code = NeedPassword.code
    return res


protect_url_space_exhaust = _short_url_exception_decorator(UrlSpaceExhaust, lambda: Response(
    UrlSpaceExhaust.content,
    UrlSpaceExhaust.api_status
))

protect_url_has_been_used = _short_url_exception_decorator(UrlHasBeenUsed, lambda: Response(
    UrlHasBeenUsed.content,
    UrlHasBeenUsed.api_status
))

url_need_password_with_api = _short_url_exception_decorator(NeedPassword, lambda: Response(
    NeedPassword.content,
    NeedPassword.api_status
))

url_need_password_with_view = _short_url_exception_decorator(NeedPassword, need_password_view_res)


def api_data_validate(serializer):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            serializer_data = serializer(data=request.data)
            if serializer_data.is_valid():
                request.validate_data = serializer_data.data
                return func(request, *args, **kwargs)
            else:
                return Response(
                    BadParams.content,
                    status=BadParams.api_status
                )

        return inner

    return decorator
