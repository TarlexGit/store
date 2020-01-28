from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from photologue.models import Gallery, Photo

from .models import Product, Category

class PhotoSer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("image",)


# class GallerySer(serializers.ModelSerializer):
#     photos = PhotoSer(many = True)
#     class Meta:
#         model = Gallery
#         fields = ("photos",)


class CatSer(serializers.ModelSerializer):
    children = serializers.ListField(source = 'get_children', read_only=True,
                                    child=RecursiveField(), )

    class Meta:
        model = Category
        fields = ('name', 'children',)

class ProductSer(serializers.ModelSerializer):
    
    photo = PhotoSer()

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'slug',
            'availability',
            'quantity',
            'photo',
        )