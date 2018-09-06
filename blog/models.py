from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset()\
                        .filter(status='published')

class Genre(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250, default="")

    def __str__ (self):
        return self.title

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    PRIORITY_CHOICES = (
        ('featured', 'Featured'),
        ('standard', 'Standard'),
        ('aside', 'Aside'),
    )
    title = models.CharField(max_length=250)
    featured_image = models.ImageField(upload_to="post-images", blank=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='draft')
    priority = models.CharField(max_length=10,
                             choices=PRIORITY_CHOICES,
                             default='standard')
    genre = models.ManyToManyField(Genre)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) #Used to toggle off inappropriate comments

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
