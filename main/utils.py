from enum import Enum
from base64 import b64decode
from collections import UserDict
import json
import binascii

from django.core import serializers

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


class UrlStruct(UserDict):
    """
    将序列化的字典形式的数据，转换为可以对象方式访问的形式
    """

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)


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


def transfer_model(origin_obj, target_model):
    obj_fields_json = serializers.serialize('json', [origin_obj])
    obj_fields_dict = json.loads(obj_fields_json)[0]['fields']
    target_model(**obj_fields_dict).save()
    origin_obj.delete()
