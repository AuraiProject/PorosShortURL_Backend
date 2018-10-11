from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404

from .shorter import shorter_runner


class BaseUrl(models.Model):
    """
    Url父类，包含一条短链记录的所有相关信息。
    expiredTime 和 password 字段是用户自定义的字段，默认情况下都为空。
    所以可以根据 expiredTime 和 password 字段是否存在判断本记录是否是用户自定义。
    """
    url = models.URLField(db_index=True)
    short_url = models.CharField(unique=True, db_index=True, max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)

    # 用户自定义的字段
    expired_time = models.DateTimeField(null=True, blank=True)
    password = models.CharField(null=True, blank=True, max_length=16)

    class Meta:
        abstract = True
        ordering = ('-created_time', 'short_url')


class Url(BaseUrl):
    @classmethod
    def to_short_url(cls, url, digit=getattr(settings, 'DEFAULT_URL_DIGIT', 4), expiredTime=None, password=None):
        """
        根据给定的原 url 和用户定义的参数，生成短url。

        :param url: 要转换为短链的原始url
        :param digit: 转换的短网址字符数
        :param expiredTime: 短链过期时间
        :param password:访问短链的密码
        :return: 短网址
        """
        return shorter_runner(cls, url, digit, expiredTime=expiredTime, password=password)

    @classmethod
    def to_origin_url(cls, short_url):
        """
        根据给定的短网址查找原 url

        :param short_url:
        :return:
        """
        url_obj = get_object_or_404(cls, short_url=short_url)
        return url_obj.url


class ExpiredUrl(BaseUrl):
    """
    到期的 url 记录将会被定期迁移到本模型。因此允许多条short_url同时存在。
    """
    short_url = models.CharField(db_index=True, max_length=255)
