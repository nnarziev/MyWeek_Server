from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^create$', views.create_custom_event),
    url(r'^categories', views.get_categorycodes),
    url(r'^predict$', views.get_prediction),
    url(r'^load_week$', views.get_events),
]

urlpatterns = format_suffix_patterns(urlpatterns)
