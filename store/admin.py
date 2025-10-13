from django.contrib import admin
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date','is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('product_name', 'category__category_name')
    list_per_page = 20
admin.site.register(Product, ProductAdmin)
