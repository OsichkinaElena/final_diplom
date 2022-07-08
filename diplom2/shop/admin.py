from django.contrib import admin
from .models import Category, Product, ProductInfo, ProductParameter, Parameter, Shop

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Parameter)
admin.site.register(ProductParameter)
admin.site.register(ProductInfo)
admin.site.register(Shop)