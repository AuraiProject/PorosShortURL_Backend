from enum import Enum
from base64 import b64decode
import binascii

from .exceptions import NeedPassword


class UrlEnum(Enum):
    EXIST_URL = 'EXIST_URL'
    NEW_SHORT_URL = 'NEW_SHORT_URL'


def need_password(url, password):
    if url.password == password:
        return True
    else:
        raise NeedPassword(url.short_url)


def get_full_short_url(request, short_code):
    return request.META['HTTP_HOST'] + '/' \
           + short_code


def get_password_from_request(request):
    authentication = request.META.get('HTTP_AUTHENTICATION', None)
    if authentication:
        b64_password = authentication.split()[-1]
        try:
            return b64_password and b64decode(b64_password.encode()).decode()
        except binascii.Error:
            return None
    return None
