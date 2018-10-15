from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .serializers import UrlSerializer, ShortUrlSerializer
from .models import Url
from .utils import get_full_short_url
from .decorators import protect_url_space_exhaust, url_need_password_with_api, url_need_password_with_view, \
    api_data_validate, protect_url_has_been_used


class UrlView(APIView):
    @url_need_password_with_api
    @api_data_validate(ShortUrlSerializer)
    def get(self, request):
        """
        从一个短网址得到完整网址
        """
        data = request.validate_data
        url_obj = Url.to_origin_url_obj(data['short_url'].split('/')[-1], data.get('password'))
        url_obj.short_url = get_full_short_url(request, url_obj.short_url)
        return Response(UrlSerializer(url_obj).data)

    @protect_url_has_been_used
    @protect_url_space_exhaust
    @api_data_validate(UrlSerializer)
    def post(self, request):
        """
        根据原网址创建一个新短网址
        """
        data = request.validate_data
        short_url_status = Url.save_short_url(data)
        url_obj = get_object_or_404(Url, short_url=short_url_status[0])
        url_obj.short_url = get_full_short_url(request, url_obj.short_url)
        return Response(UrlSerializer(url_obj).data)


@url_need_password_with_view
def redirect_url(request, short_url):
    url_obj = Url.to_origin_url_obj(short_url, request.POST.get('password'))
    return HttpResponseRedirect(url_obj.url)
