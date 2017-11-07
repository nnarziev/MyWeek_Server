from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^create$', views.create_event),
    url(r'^categories', views.get_categorycodes),
    url(r'^suggest$', views.get_suggestion),
    url(r'^fetch$', views.get_events),
    url(r'^disable$', views.disable_event),
    url(r'^flushdb$', views.flushdb),
    url(r'^populate$', views.populate),
]

urlpatterns = format_suffix_patterns(urlpatterns)
