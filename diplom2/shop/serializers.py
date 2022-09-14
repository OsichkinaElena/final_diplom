from rest_framework import serializers
from shop.models import Product, Category, ProductInfo, Shop
from orders_.models import CartProduct, Cart, Contact


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    # shop = ProductInfo.objects.all()

    class Meta:
        model = Product
        fields = ['name', 'category', ]


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'url', ]


class ProductListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()
    class Meta:
        model = ProductInfo
        fields = ['model', 'external_id', 'product', 'shop', 'quantity', 'price', 'price_rrc']




