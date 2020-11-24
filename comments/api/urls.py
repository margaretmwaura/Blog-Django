from django.conf.urls import url

from .views import (
    CommentListApiView,
    CommentDetailApiView,
    CommentCreateApiView,
)
urlpatterns = [
    url(r'^$',CommentListApiView.as_view(), name='list'),
    url(r'^create/$',CommentCreateApiView.as_view(), name='create'),
    url(r'^(?P<id>\d+)/$',CommentDetailApiView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/edit/$',CommentEditApiView.as_view(), name='edit'),
]