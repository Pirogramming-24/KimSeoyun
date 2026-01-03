from django.db import models

# Create your models here.


class DevTool(models.Model):
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=200)
    content = models.TextField()

class Idea(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to="ideas/", blank=True, null=True)
    content = models.TextField()
    interest = models.IntegerField()
    devtool = models.CharField(max_length=200)
    starred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      