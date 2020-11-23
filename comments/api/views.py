from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
    )


from .serializers import (
    CommentSerializer,
    CommentDetailSerializer
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from posts.api.permissions import IsOwnerOrReadOnly

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from comments.models import Comment 

# class PostCreateApiView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class CommentListApiView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['content','user__first_name']
    pagination_class = PostPageNumberPagination 

    def get_queryset(self, *args, **kwargs):
        query_set_list = Comment.objects.all()
        # query_set_list = super(PostListApiView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')

        if query:
            query_set_list = query_set_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query)
                ).distinct()

        return query_set_list

# class PostUpdateApiView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)

# class PostDeleteApiView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class CommentDetailApiView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'id'
