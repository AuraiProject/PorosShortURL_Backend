from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .serializers import UrlSerializer, ShortUrlSerializer
from .models import Url
from .utils import get_full_short_url
from .decorators import protect_url_space_exhaust, url_need_password_with_api, url_need_password_with_view, \
    api_data_validate, protect_url_has_been_used


@api_view(['POST'])
@protect_url_has_been_used
@protect_url_space_exhaust
@api_data_validate(UrlSerializer)
def long_to_short(request):
    data = request.validate_data
    short_url_status = Url.save_short_url(data)
    url_cls = get_object_or_404(Url, short_url=short_url_status[0])
    url_cls.short_url = get_full_short_url(request, url_cls.short_url)
    return Response(UrlSerializer(url_cls).data)


@api_view(['POST'])
@url_need_password_with_api
@api_data_validate(ShortUrlSerializer)
def short_to_long(request):
    data = request.validate_data
    url_obj = Url.to_origin_url_obj(data['short_url'].split('/')[-1], data.get('password'))
    url_obj.short_url = get_full_short_url(request, url_obj.short_url)
    url_serialization = UrlSerializer(url_obj)
    return Response(
        url_serialization.data
    )


@url_need_password_with_view
def redirect_url(request, short_url):
    url_obj = Url.to_origin_url_obj(short_url, request.POST.get('password'))
    return HttpResponseRedirect(url_obj.url)
