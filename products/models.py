from django.db import models
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    level = models.PositiveIntegerField(default=1)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.category_name))
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    product_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s грн." % (self.product_name, self.price)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.product_name))
        super(Product, self).save(*args, *kwargs)

    def discount_price(self):
        price = self.price * 100 / self.discount
        return price

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    option_name = models.CharField(max_length=100)
    option_slug = models.SlugField(max_length=100)
    option_value = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} - {}'.format(self.product.product_name, self.option_name, self.option_value)

    def save(self, *args, **kwargs):
        self.option_slug = slugify(unidecode(self.option_name))
        super(ProductDetail, self).save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    active = models.BooleanField(default=True)
    main = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        string = "Image of {product}".format(product=self.product.product_name)
        if self.main:
            string = "Main image of {product}".format(product=self.product.product_name)
        return string

