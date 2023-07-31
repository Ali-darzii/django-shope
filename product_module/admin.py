from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['title', 'category', 'is_active']
    list_display = ['id', 'title',  'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)