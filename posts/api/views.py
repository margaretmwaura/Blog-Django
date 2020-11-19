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

from posts.models import Post

from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, 
    PostCreateUpdateSerializer, 
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from .permissions import IsOwnerOrReadOnly

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostListApiView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','content','user__first_name']
    pagination_class = PostPageNumberPagination 

    def get_queryset(self, *args, **kwargs):
        query_set_list = Post.objects.all()
        # query_set_list = super(PostListApiView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')

        if query:
            query_set_list = query_set_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query)
                ).distinct()

        return query_set_list

class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
