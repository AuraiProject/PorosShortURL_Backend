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
    def short_url_is_available(url_cls, url, short_url):
        try:
            url_obj = url_cls.objects.get(short_url=short_url)
        except url_cls.DoesNotExist:
            return short_url, UrlEnum.NEW_SHORT_URL
        else:
            if url == url_obj.url:
                # 如果是目标url，直接返回
                return short_url, UrlEnum.EXIST_URL
            else:
                # 否则返回 None 以表示发生了url冲突
                return None

    def generate(self, *args, **kwargs):
        raise NotImplementedError()


class HashQueryShorter(BaseShorter):
    @classmethod
    def generate(cls, url_cls, url, digit, **params):
        """
        根据给定的信息实际生成一个短链。

        :param url_cls: 保存 url 记录的类
        :param url: 原始链接
        :param digit: 要生成短链的位数
        :param params: 自定义信息，给出自定义信息，相同 url 每次会生成不一样的短链。反之，若 params 里值全为
        None，会生成同一个的短链。
        :return: 返回一个两个元素的元组。第一个代表此次生成的短链。第二个指示这个短链是新生成的，还是已经存在的，即，
        params 全为None时生成的短链。
        """
        short_url = params.get('short_url')
        if short_url:
            return cls.specify_url(url_cls, short_url)
        else:
            if not digit:
                raise ValueError()

            # 为了保证不同自定义参数的 url 生成的短链也不同
            url_md5 = cls.hash_url(url + repr(params))

            total_ch_ord = 0
            short_url = []
            # index 是查 url md5 的开始位置。如果 index 为 0，那么指定不同 digit 的短链很可能拥有相同
            # 的前缀，带有安全隐患。为了规避这一点，将 index 设为 digit 的值，这样，不同 digit 生成的短链也会完全不一样
            index = digit
            while True:
                for ch in url_md5[index: index + digit]:
                    total_ch_ord += ord(ch)
                    short_url.append(URL_CHAR_TABLE[total_ch_ord % len(URL_CHAR_TABLE)])
                short_url = ''.join(short_url)
                result = cls.short_url_is_available(url_cls, url, short_url)
                if not result:
                    # 生成的短链已经存在，重新生成
                    short_url = []
                    index += digit
                    if index + digit > len(url_md5):
                        # 用尽了md5 32位字符仍然无法生成一个没有冲突的短链
                        raise UrlSpaceExhaust()
                else:
                    return result


shorter_runner = HashQueryShorter.generate
