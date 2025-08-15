from django.db import models
from django.contrib.auth.models import User
from products.models import Products
# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        return self.product.product_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} for {self.user.username}"
    
