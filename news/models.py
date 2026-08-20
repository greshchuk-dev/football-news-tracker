from django.db import models

# Create your models here.
class NewsArticle(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=200, unique=True)
    url_to_image = models.URLField(max_length=200, null=True, blank=True)
    published_at = models.DateTimeField(unique=True)
    content = models.TextField(null=True, blank=True)
    source_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title