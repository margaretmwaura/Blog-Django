from django.db.models import Q

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

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
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
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

class CommentCreateApiView(CreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
            model_type = model_type, 
            slug = slug,
            parent_id = parent_id,
            user = self.request.user
            )

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class CommentListApiView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['content','user__first_name']
    pagination_class = PostPageNumberPagination 

    def get_queryset(self, *args, **kwargs):
        query_set_list = Comment.objects.filter(id__gte=0)
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

# class CommentEditApiView(RetrieveAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetailSerializer
#     lookup_field = 'id'


class CommentDetailApiView(DestroyModelMixin, UpdateModelMixin,  RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    # serializer_class = CommentEditSerializer
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

