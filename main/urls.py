from django.urls import path

from .views import UrlView, redirect_url

app_name = 'api'
urlpatterns = [
    path('api/url', UrlView.as_view()),

    path('<short_url>', redirect_url)
]
