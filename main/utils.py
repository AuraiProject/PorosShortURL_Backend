from enum import Enum

from .exceptions import NeedPassword


class UrlEnum(Enum):
    EXIST_COMMON_URL = 'EXIST_COMMON_URL'
    NEW_SHORT_URL = 'NEW_SHORT_URL'


def need_password(url, password):
    if url.password == password:
        return True
    else:
        raise NeedPassword()


def get_full_short_url(request, short):
    return request.scheme + '://' \
           + request.META['HTTP_HOST'] + '/' \
           + short
