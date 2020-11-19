from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

# from rest_framework import serializers.HyperLinkedIdentityField

from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish'
        ]

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='posts-api:delete',
        lookup_field='slug'
    )
    class Meta:
        model = Post
        fields = [
            'url',
            'delete_url',
            'id' ,
            'title',
            'slug',
            'content',
            'publish',
            'user'
        ]


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'publish'
        ]