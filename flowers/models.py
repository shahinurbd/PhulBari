from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Flower(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    tag = models.CharField(max_length=10, blank=True, null=True)
    isNew = models.BooleanField(default=True, blank=True, null=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='flowers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id',]

    def __str__(self):
        return self.name
    

class FlowerImage(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')

