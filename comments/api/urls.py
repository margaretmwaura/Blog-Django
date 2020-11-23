from django.conf.urls import url

from .views import (
    CommentListApiView,
    CommentDetailApiView
)
urlpatterns = [
    url(r'^$',CommentListApiView.as_view(), name='list'),
    url(r'^(?P<id>\d+)/$',CommentDetailApiView.as_view(), name='delete'),
]