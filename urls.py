from django.conf.urls import url
from django.urls import include, path
import BetterClassFinder.api

urlpatterns = [
    path('api/', BetterClassFinder.api.get_courses)
]
