"""
存放以不同缩短网址算法实现的不同生成短网址的类。
以 shorter_runner 的形式公开出其中一个供外部使用。
"""
import hashlib
import string

from .exceptions import UrlSpaceExhaust, UrlHasBeenUsed
from .utils import UrlEnum

URL_CHAR_TABLE = string.ascii_letters + string.digits


class BaseShorter:
    @staticmethod
    def specify_url(url_cls, short_url):
        try:
            url_cls.objects.get(short_url=short_url)
        except url_cls.DoesNotExist:
            return short_url, UrlEnum.NEW_SHORT_URL
        else:
            raise UrlHasBeenUsed

    @staticmethod
    def hash_url(url):
        return hashlib.md5(url.encode()).hexdigest()

    @staticmethod
    def short_url_is_available(url_cls, url, short_url, params):
        try:
            url_obj = url_cls.objects.get(short_url=short_url)
        except url_cls.DoesNotExist:
            return short_url, UrlEnum.NEW_SHORT_URL
        else:
            # 如果是目标url，并且不是自定义短链，直接返回
            # 否则发生了url冲突
            if url == url_obj.url and not any(params.values()):
                return short_url, UrlEnum.EXIST_COMMON_URL

        return None

    def generate(self, *args, **kwargs):
        raise NotImplementedError()


class HashQueryShorter(BaseShorter):
    @classmethod
    def generate(cls, url_cls, url, digit, **params):
        short_url = params.get('short_url')
        if short_url:
            return cls.specify_url(url_cls, short_url)
        else:
            if not digit:
                raise ValueError()

            # 为了保证不同自定义参数的 url 生成的短链也不同
            url_md5 = cls.hash_url(url + repr(params))

            index = 0
            total_ch_ord = 0
            short_url = []
            while True:
                for ch in url_md5[index: index + digit]:
                    total_ch_ord += ord(ch)
                    short_url.append(URL_CHAR_TABLE[total_ch_ord % len(URL_CHAR_TABLE)])
                short_url = ''.join(short_url)
                result = cls.short_url_is_available(url_cls, url, short_url, params)
                if not result:
                    short_url = []
                    index += digit
                    if index + digit > len(url_md5):
                        # 用尽了md5 32位字符仍然无法生成一个没有冲突的短链
                        raise UrlSpaceExhaust()
                else:
                    return result


shorter_runner = HashQueryShorter.generate
