from datetime import datetime
import json

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core import serializers

from .shorter import shorter_runner
from .utils import need_password, UrlEnum


class BaseUrl(models.Model):
    """
    Url父类，包含一条短链记录的所有相关信息。
    expiredTime 和 password 字段是用户自定义的字段，默认情况下都为空。
    所以可以根据 expiredTime 和 password 字段是否存在判断本记录是否是用户自定义。
    """
    url = models.URLField(db_index=True)
    short_url = models.CharField(unique=True, db_index=True, max_length=255)
    created_time = models.IntegerField()  # timestamp

    # 用户自定义的字段
    expired_time = models.IntegerField(null=True, blank=True)  # timestamp
    password = models.CharField(null=True, blank=True, max_length=16)

    class Meta:
        abstract = True
        ordering = ('-created_time', 'short_url')


class FilterExpiredUrlManager(models.Manager):
    """
    从 queryset 中过滤过期的 url 记录。
    为了避免数据库竟态，只在查询时做过滤，不实际迁移。
    """

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(expired_time__gte=datetime.timestamp(datetime.now())) |
            Q(expired_time__isnull=True)
        )


class Url(BaseUrl):
    """
    当前有效的 Url 记录.
    """

    objects = FilterExpiredUrlManager()

    def save(self, *args, **kwargs):
        """
        因为 FilterExpiredUrlManager 过滤了过期的记录，因此，即使 filter 不到某条指定 short_url 的记录，
        该记录也可能以过期 url 的记录存在于表中。所以保存时需要将此过期的 url 记录迁移到 ExpiredUrl 表，以保存新记录.

        因为只有在访问到某个过期记录的时候才会清理，为了防止某些久不被访问的过期记录一直占用空间，仍需要定期
        执行额外的清理任务。
        """
        try:
            expired_url_cls = self.__class__._base_manager.get(short_url=self.short_url)
        except self.__class__.DoesNotExist:
            pass
        else:
            expired_url_fields_json = serializers.serialize('json', [expired_url_cls])
            expired_url_fields_dict = json.loads(expired_url_fields_json)[0]['fields']
            ExpiredUrl(**expired_url_fields_dict).save()
            expired_url_cls.delete()

        self.created_time = datetime.timestamp(datetime.now())
        return super().save()

    @classmethod
    def to_short_url(cls, url=None, digit=getattr(settings, 'DEFAULT_URL_DIGIT', 4), short_url=None, expired_time=None,
                     password=None):
        """
        根据给定的原 url 和用户定义的参数，生成短url。

        :param url: 要转换为短链的原始url
        :param digit: 转换的短网址字符数
        :param short_url: 指定要使用的short_url
        :param expiredTime: 短链过期时间
        :param password:访问短链的密码
        :return: 短网址
        """
        return shorter_runner(cls, url, digit, short_url=short_url, expiredTime=expired_time, password=password)

    @classmethod
    def to_origin_url_obj(cls, short_url, password=None):
        """
        根据给定的短网址查找原 url

        :param short_url:
        :return:
        """
        url_obj = get_object_or_404(cls, short_url=short_url)
        need_password(url_obj, password)
        return url_obj

    @classmethod
    def save_short_url(cls, data):
        """
        根据传入的参数存入短链

        :param data: 参数参数的字典
        :return: 生成 url 的状态
        """
        short_url_status = cls.to_short_url(**data)

        if short_url_status[1] == UrlEnum.NEW_SHORT_URL:
            data['short_url'] = short_url_status[0]
            try:
                data.pop('digit')
            except KeyError:
                pass
            finally:
                url = Url(**data)
                url.save()

        return short_url_status


class ExpiredUrl(BaseUrl):
    """
    到期的 url 记录将会被定期迁移到本模型。因此允许多条short_url同时存在。
    """
    short_url = models.CharField(db_index=True, max_length=255)
