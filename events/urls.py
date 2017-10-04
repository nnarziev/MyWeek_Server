from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^create$', views.create_custom_event)
]

urlpatterns = format_suffix_patterns(urlpatterns)