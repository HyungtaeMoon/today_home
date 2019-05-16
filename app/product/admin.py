from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Company, CartItem, Comment


@admin.register(Product)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['photo_tag', 'name', 'price']

    list_display_links = ['name']

    def photo_tag(self, item):
        if item.image:
            return mark_safe('<img src={} style="width: 75px;"/>'.format(item.image.url))
        return None


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'image', 'created_at']
