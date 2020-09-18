from django.conf.urls import url

from .views import (
    post_list,
    post_detail,
)
urlpatterns = [
    url(r'^$',post_list),
    url(r'^(?P<id>\d+)/$',post_detail),
]