from django.urls import path

from .views import UrlView, redirect_url, react_app

app_name = 'api'
urlpatterns = [
    path('', react_app),
    path('api/url', UrlView.as_view()),
    path('<short_url>', redirect_url)
]
