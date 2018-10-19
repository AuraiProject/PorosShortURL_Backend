from enum import Enum
from base64 import b64decode
import binascii

from .exceptions import NeedPassword

# 因为本站业务的特殊性，能够根据提交的路径进行重定向，且路径能够被用户指定。后端固有的路由优先级高于用户创建的路由（短链）
# ，因此无需处理，然而前端的路由可能会被覆盖。因此，在这里声明前端所使用的路由，这些路由会在程序启动时动态注册到路由表。
DANGER_PATH = [
    'restore',
    'api',
    'check',
]


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
