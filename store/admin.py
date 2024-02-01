from django.contrib import admin
import admin_thumbnails
from .models import *


# Adding fields on admin panel

# User Admin Field
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone_number']


@admin_thumbnails.thumbnail('image')
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortInfo', 'owner', 'phone', 'image_tag']


# Color Admin Fields
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


# Category Admin fields
@admin_thumbnails.thumbnail('image')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'image_tag']
    search_fields = ['name']


# Brand Admin Fields
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# ProductImage Admin Field
class ProductsImageAdmin(admin.StackedInline):
    model = ProductsImage
    extra = 1


class ProductVariantAdmin(admin.TabularInline):
    model = ProductVariant
    extra = 1


# Product Admin Field
@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'sell_price', 'is_available', 'image_tag']
    search_fields = ['name', 'category__name', 'brand__name']
    list_filter = ['category__name', 'brand', 'is_available']
    list_editable = ['is_available']
    inlines = [ProductsImageAdmin, ProductVariantAdmin]


# Registration models
admin.site.register(User, UserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Currency)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Option)
admin.site.register(OptionValue)
admin.site.register(ProductVariant)
