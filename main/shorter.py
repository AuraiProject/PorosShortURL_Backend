"""
存放以不同缩短网址算法实现的不同生成短网址的类。
以 shorter_runner 的形式公开出其中一个供外部使用。
"""
import hashlib
import string

from .exceptions import UrlSpaceExhaust

URL_CHAR_TABLE = string.ascii_letters + string.digits


class HashQueryShorter:
    @classmethod
    def generate(cls, url_cls, url, digit, **params):
        # 为了保证不同自定义参数的 url 生成的短链也不同
        url += repr(params)
        url_md5 = hashlib.md5(url.encode()).hexdigest()

        index = 0
        short_url = []
        while True:
            for ch in url_md5[index: index + digit]:
                short_url.append(URL_CHAR_TABLE[ord(ch) % len(URL_CHAR_TABLE)])
            short_url = ''.join(short_url)
            try:
                url_cls.objects.get(short_url=short_url)
            except url_cls.DoesNotExist:
                return short_url
            else:
                short_url = []
                index += digit
                if index + digit > len(url_md5):
                    raise UrlSpaceExhaust()


shorter_runner = HashQueryShorter.generate
