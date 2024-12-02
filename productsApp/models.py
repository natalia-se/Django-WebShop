from django.db import models

# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     image = models.ImageField(upload_to='product_images/')
#     cake_details = models.CharField(max_length=300)
#     weight = models.CharField(max_length=50)

class Cake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/')  # Requires Pillow library
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
