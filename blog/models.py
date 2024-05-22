from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DFAFT = 'DF','Draft'
        PUBLISHED = 'PB', 'Published'

    title  = models.CharField(max_length=250)
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='cat_post')
    image = models.ImageField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    status= models.CharField(max_length=2,choices=Status.choices,default=Status.DFAFT)
    body = models.TextField()
    slug = models.SlugField(max_length=250)
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishManager()

    @property
    def category_count(self):
        return Category.objects.filter(post = self).count()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['publish'])
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail_page',args =[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='cat_post')

    

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('detail_page',args =[self.slug])

    def __str__(self):
        return self.body
