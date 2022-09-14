from rest_framework import serializers
from shop.models import Product, Category, ProductInfo, Shop
from orders_.models import CartProduct, Cart, Customer
from shop.serializers import ProductSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartProduct
        fields = ['product', 'qty', 'total_price', 'shop']

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = '__all__'

    @staticmethod
    def get_user(obj):
        first_name = obj.user.first_name
        last_name = obj.user.last_name
        if not (first_name and last_name):
            return obj.user.username
        return ''.join([first_name, last_name])


class CartSerializer(serializers.ModelSerializer):

    products = CartProductSerializer(many=True)
    owner = CustomerSerializer()

    class Meta:
        model = Cart
        fields = '__all__'