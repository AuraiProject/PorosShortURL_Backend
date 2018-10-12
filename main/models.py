from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404

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
    created_time = models.DateTimeField(auto_now_add=True)

    # 用户自定义的字段
    expired_time = models.IntegerField(null=True, blank=True)  # 存放timestamp
    password = models.CharField(null=True, blank=True, max_length=16)

    class Meta:
        abstract = True
        ordering = ('-created_time', 'short_url')


class Url(BaseUrl):
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
