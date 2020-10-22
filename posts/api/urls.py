from django.conf.urls import url

from posts.api.views import (
    PostListApiView,
)
urlpatterns = [
    url(r'^$',PostListApiView.as_view(), name='list'),
    # url(r'^(?P<id>\d+)/$',post_detail, name='detail'),
    # url(r'^create/$',post_create),
    # url(r'^(?P<id>\d+)/delete/$',post_delete),
    # url(r'^(?P<id>\d+)/update/$',post_update, name='update'),
]