from django.urls import path, re_path

from .views import UrlView, redirect_url, react_app

app_name = 'api'
urlpatterns = [
    path('<short_url>', redirect_url),
    path('api/url', UrlView.as_view()),
    re_path('^$', react_app),
]
