from django.urls import path, re_path

from .views import UrlView, redirect_url, react_app
from .danger import DANGER_PATH


def make_urlpatterns_safe(urlpatterns):
    """
    防止前端路由被生成的短链覆盖，将它们注册到 urlpatterns 最前面
    """
    for danger_path in DANGER_PATH:
        urlpatterns.insert(0, path(danger_path, react_app))
    return urlpatterns


app_name = 'api'
urlpatterns = make_urlpatterns_safe(
    [
        path('api/url', UrlView.as_view()),
        path('<short_url>', redirect_url),
        re_path('^$', react_app),
    ]
)
