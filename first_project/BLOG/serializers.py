from rest_framework import serializers
from . import models 

class BlogUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.BlogUser
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)



