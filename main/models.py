from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode

# Create your models here.
class MarketInfo(models.Model):
    info_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    info_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.info_name))
        super(MarketInfo, self).save(*args, **kwargs)

class Slide(models.Model):
    slide_name = models.CharField(max_length=155)
    slide_slug = models.SlugField(max_length=155)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    url_to = models.URLField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)