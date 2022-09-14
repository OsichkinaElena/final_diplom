from django.contrib import admin
from .models import Category, Product, ProductInfo, ProductParameter, Parameter, Shop


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['model', 'external_id', 'price', 'product', 'shop', 'quantity', 'price_rrc']
    list_filter = ['shop']
admin.site.register(ProductInfo, ProductInfoAdmin)


admin.site.register(Parameter)
admin.site.register(ProductParameter)
admin.site.register(Shop)