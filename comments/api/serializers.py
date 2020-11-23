
from django.contrib.contenttypes.models import ContentType

from rest_framework.serializers import ( 
    ModelSerializer,
    HyperlinkedIdentityField, 
    SerializerMethodField,
)

# from rest_framework import serializers.HyperLinkedIdentityField

from comments.models import Comment

def create_comment_serializer(model_type='post', slug='None', parent_id=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
        model = Comment
        fields = [
            'id',
            'parent',
            'content',
        ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if self.parent_id:
                parent_qs = Comment.objects.filter(id = parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model = model_type)

    return CommentCreateSerializer



class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
 
    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count'
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp'
        ]



class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'replies',
            'timestamp',
            'reply_count'
        ]

    def get_replies(self, object):
        if object.is_parent:
            return CommentChildSerializer(object.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

