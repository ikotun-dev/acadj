from django.db import models

# Create your models here.
class BlogUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    postTitle = models.CharField(max_length=255, null=False)
    postContent = models.CharField(max_length=255, null=False)
    postOwner = models.ForeignKey(BlogUser, on_delete=models.CASCADE, null=True)
    



