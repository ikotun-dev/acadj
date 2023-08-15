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

class Hirer(models.Model) : 
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)

class Freelancer(models.Model) : 
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)

class Job(models.Model) : 
    id = models.AutoField(primary_key=True)
    jobTitle = models.CharField(max_length=255, null=False)
    jobDescription = models.CharField(max_length=255, null=False)
    jobOwner = models.ForeignKey(Hirer, on_delete=models.CASCADE, null=True)
