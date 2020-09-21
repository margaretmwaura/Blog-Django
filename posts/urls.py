from django.conf.urls import url

from .views import (
    post_list,
    post_detail,
    post_create,
    post_delete,
    post_update,
)
urlpatterns = [
    url(r'^$',post_list, name='list'),
    url(r'^(?P<id>\d+)/$',post_detail, name='detail'),
    url(r'^create/$',post_create),
    url(r'^(?P<id>\d+)/delete/$',post_delete),
    url(r'^(?P<id>\d+)/update/$',post_update, name='update'),
]