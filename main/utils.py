from enum import Enum

from .exceptions import NeedPassword


class UrlEnum(Enum):
    EXIST_URL = 'EXIST_URL'
    NEW_SHORT_URL = 'NEW_SHORT_URL'


def need_password(url, password):
    if url.password == password:
        return True
    else:
        raise NeedPassword()


def get_full_short_url(request, short_code):
    return request.scheme + '://' \
           + request.META['HTTP_HOST'] + '/' \
           + short_code
