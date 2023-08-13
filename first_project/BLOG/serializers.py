from rest_framework import serializers
from . import models 

class BlogUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.BlogUser
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)

class PostSerializer(serializers.ModelSerializer):
    postOwner = serializers.SerializerMethodField()

    class Meta : 
        model = models.Post
        fields = ('id', 'postTitle', 'postContent', 'postOwner')
        read_only_fields = ('id',)

    def get_postOwner(self, obj):
        return obj.postOwner.username