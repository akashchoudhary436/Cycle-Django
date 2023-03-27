from django.db import models
from django.utils.text import slugify


# Create your models here.

class Contact(models.Model):
    s_no = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)
    Email = models.EmailField(max_length=50)
    Contact = models.CharField(max_length=10)
    Subject = models.CharField(max_length=50)
    Message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.Name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    product_name = models.CharField(max_length=50)

    product_price = models.IntegerField()
    product_quantity = models.IntegerField()
    image = models.ImageField(upload_to="media")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name
