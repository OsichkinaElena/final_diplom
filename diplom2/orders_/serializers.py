from rest_framework import serializers
from shop.models import Product, Category, ProductInfo, Shop
from orders_.models import OrderItem, Order #CartProduct, Cart, Customer
from shop.serializers import ProductSerializer, ProductInfoSerializer
from account.serializers import ContactSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order')
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'status', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)


# class CartProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     class Meta:
#         model = CartProduct
#         fields = ['product', 'qty', 'total_price', 'shop']
#
# class CustomerSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     class Meta:
#         model = Customer
#         fields = '__all__'
#
#     @staticmethod
#     def get_user(obj):
#         first_name = obj.user.first_name
#         last_name = obj.user.last_name
#         if not (first_name and last_name):
#             return obj.user.username
#         return ''.join([first_name, last_name])
#
#
# class CartSerializer(serializers.ModelSerializer):
#
#     products = CartProductSerializer(many=True)
#     owner = CustomerSerializer()
#
#     class Meta:
#         model = Cart
#         fields = '__all__'