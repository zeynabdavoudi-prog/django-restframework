from django.db import models
from accounts.models import Profile
from django.urls import reverse


class Post(models.Model):
    """
    this is a class to define posts for blog app
    """
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255)
    context = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ManyToManyField("Category", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

    def Snippet(self):
        return f'{self.context[:5]}...'

    def get_absolute_api_url(self):
        return reverse('blog:api-v1:post-detail', kwargs={'pk': self.id})


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
