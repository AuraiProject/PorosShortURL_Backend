from django.urls import path

from .views import long_to_short, short_to_long, redirect_url

app_name = 'api'
urlpatterns = [
    path('long_to_short', long_to_short),
    path('short_to_long', short_to_long),

    path('<short_url>', redirect_url)
]
