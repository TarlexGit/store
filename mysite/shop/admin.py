from django.contrib import admin
from django import forms 

from mptt.admin import MPTTModelAdmin

from photologue.models import Gallery, Photo
from photologue.admin import GalleryAdmin as GalleryAdminDefault

from .models import (Category, Product)
# from mysite.shop.services import services

# Register your models here.

class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20 
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryMPTTModelAdmin)   

class ProductAdmin(admin.ModelAdmin):
    """Продукты"""
    list_display = ('title', 'category', 'price', 'quantity')
    preropulated_fields = {'slug': ('titule',)}

admin.site.register(Product, ProductAdmin)

class Admin(admin.ModelAdmin):
    """Товары в корзине"""
    list_display = ('cart', 'product', 'quantity')
    
class GallaryAdminForm(forms.ModelForm):
    class Meta: 
        model = Gallery
        exclude = ['description']

class GalaryAdmin(GalleryAdminDefault):
    form = GallaryAdminForm