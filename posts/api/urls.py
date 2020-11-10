from django.conf.urls import url

from posts.api.views import (
    PostListApiView,
    PostDetailApiView,
    PostUpdateApiView,
    PostDeleteApiView,
    PostCreateApiView
)

# Something to note if the detail url is before the create url the create url will never be resolved
# for the create word will be treated as a slug 
urlpatterns = [
    url(r'^$',PostListApiView.as_view(), name='list'),
    url(r'^create/$',PostCreateApiView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$',PostDetailApiView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/delete/$',PostDeleteApiView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/update/$',PostUpdateApiView.as_view(), name='update'),
]