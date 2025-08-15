from django.db import models
from django.contrib.auth.models import User

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField(blank=True)
    product_category = models.CharField(max_length=100)
    product_bestseller = models.BooleanField(default=False)
    product_tranding = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product_name} - {self.product_price} - {self.product_category} - {self.product_bestseller}'

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Image for {self.product.product_name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.product_name}'

