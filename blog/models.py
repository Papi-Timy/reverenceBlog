from typing import ChainMap
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import SlugField
from django.db.models.signals import pre_save
from django.urls import reverse
from tinymce.models import HTMLField
from reverence.utils import unique_slug_generator

User = get_user_model()


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post',  on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_app:category", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    description = models.CharField(max_length=200, default="I love you ")
    slug = models.SlugField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    content = HTMLField()

    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_app:post-detail", kwargs={"slug": self.slug})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def get_update(self):
        return reverse("blog_app:post-update", kwargs={"id": self.pk})

    @property
    def get_delete(self):
        return reverse("blog_app:post-delete", kwargs={"id": self.pk})

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class SignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Qoutes(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.author


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def slug_cat_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)
pre_save.connect(slug_cat_generator, sender=Category)
