import json
from uuid import uuid4
from functools import update_wrapper
from datetime import datetime

from django_redis import get_redis_connection
from django.core.serializers import serialize
from django.conf import settings
from django.http import Http404

from .utils import need_password, UrlStruct


class AccessCache:
    redis = get_redis_connection()
    prefix = 'access:'

    @classmethod
    def _set_log(cls, short_url):
        cls.redis.zadd(cls.prefix + short_url, datetime.timestamp(datetime.now()), uuid4())

    @classmethod
    def _del_overtime(cls, short_url):
        now_timestamp = datetime.timestamp(datetime.now())
        overtime_interval = getattr(settings, "URL_CACHE_INTERVAL", 60 * 60)
        return cls.redis.zremrangebyscore(cls.prefix + short_url, 0, now_timestamp - overtime_interval)

    @classmethod
    def _get_access_num(cls, short_url):
        return cls.redis.zcard(cls.prefix + short_url)

    @classmethod
    def log(cls, short_url):
        """
        记录一个针对指定短链的访问记录
        """
        cls._set_log(short_url)
        cls._del_overtime(short_url)

    @classmethod
    def should_cache(cls, short_url):
        """
        根据单位时间内的访问数量判断指定短链是否应该被缓存
        """
        num = cls._get_access_num(short_url)
        limitation = getattr(settings, "MIN_CACHE_ACCESS_NUM", 10)
        return num > limitation


class UrlCache:
    redis = get_redis_connection()
    prefix = "url:"

    @classmethod
    def _get_cache(cls, short_url):
        return cls.redis.get(cls.prefix + short_url)

    @classmethod
    def _set_cache(cls, short_url, content):
        cls.redis.set(cls.prefix + short_url, content)

    @classmethod
    def _del_cache(cls, short_url):
        cls.redis.delete(short_url)

    @classmethod
    def get_cache(cls, short_url, password):
        """
        尝试得到指定短链的缓存。如果没有缓存就返回None。
        """
        url_obj_serialize = cls._get_cache(short_url)
        if not url_obj_serialize:
            return None
        else:
            url_obj = UrlStruct(json.loads(url_obj_serialize)[0]['fields'])
            if getattr(url_obj, "expired_timestamp", None) \
                    and url_obj.expired_timestamp < datetime.timestamp(datetime.now()):
                cls._del_cache(short_url)
                raise Http404
            need_password(url_obj, password)
            return url_obj

    @classmethod
    def set_cache(cls, short_url, url_obj):
        """
        将short_url的缓存设置为url_obj
        """
        url_obj_serialize = serialize('json', [url_obj])
        cls._set_cache(short_url, url_obj_serialize)

    @classmethod
    def del_cache(cls, short_url):
        """
        删去short_url的缓存
        """
        cls._del_cache(short_url)

    @classmethod
    def cache(cls, func):
        def decorator(wrapped_cls, short_url, password=None):
            AccessCache.log(short_url)
            should_cache = AccessCache.should_cache(short_url)
            url_obj = cls.get_cache(short_url, password)
            if not url_obj:
                url_obj = func(wrapped_cls, short_url, password=password)
                if should_cache:
                    cls.set_cache(short_url, url_obj)
            if not should_cache:
                cls.del_cache(short_url)
            return url_obj

        decorator = update_wrapper(decorator, func)
        return decorator
