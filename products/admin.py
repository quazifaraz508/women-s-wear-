from django.contrib import admin
from .models import Products, ProductImage, Favorite
from django.core.exceptions import ValidationError

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    min_num = 2
    max_num = 5

class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Products, ProductsAdmin)
admin.site.register(Favorite)
