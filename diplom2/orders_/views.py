from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import response, status, viewsets
from .serializers import CartSerializer
from .models import Cart, CartProduct, Product, Customer


class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    queryset = Cart.objects.all()


    @staticmethod
    def get_cart(user):
        if user.is_authenticated:
            return Cart.objects.filter(owner=user.customer, for_anonymus_user=False).first()
        return Cart.objects.filter(for_anonymus_user=True).first()


    @staticmethod
    def get_or_create_cp(customer: Customer, cart: Cart, product: Product):
        cart_product, created = CartProduct.objects.get_or_create(
            user=customer,
            product=product,
            cart=cart
        )
        return cart_product, created

    @action(methods=['get'], detail=False)
    def current_customer_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        cart_serializer = CartSerializer(cart)
        return response.Response(cart_serializer.data)


    @action(methods=["put"], detail=False, url_path='current_customer_cart/add_to_cart/(?P<product_id>\d+)')
    def add_to_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart_product, created = self.get_or_create_cp(self.request.user.customer, cart, product)
        if created:
            cart.products.add(cart_product)
            cart.save()
            return response.Response({'detail': 'Товар добавлен в корзину'})
        return response.Response({'detail': 'Товар уже в корзине'}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['path'], detail=False, url_path='current_customer_cart/change_qty/(?P<qty>\d+)/(?P<cart_product_id>\d+)')
    def product_change_qty(self, *args, **kwargs):
        cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
        cart_product.qty = int(kwargs['qty'])
        cart_product.save()
        cart_product.cart.save()
        return response.Response(status=status.HTTP_200_OK)


    @action(methods=['put'], detail=False,
            url_path='current_customer_cart/remove_from_cart/(?P<cart_product_id>\d+)')
    def product_remove_from_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
        cart_products.remove(cart_product)
        cart_product.delete()
        cart.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)