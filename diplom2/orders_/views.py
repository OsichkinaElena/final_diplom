from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import response, status, viewsets
from .serializers import OrderSerializer, OrderItemSerializer, OrderItemCreateSerializer #CartSerializer
from .models import Product, Order, OrderItem #Cart, CartProduct,  Customer
from account.models import Contact
from rest_framework.views import APIView


class CartView(APIView):
    """
    Класс для работы с корзиной пользователя
    """
    throttle_scope = 'user'

    # получить корзину
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)
        cart = Order.objects.filter(
            user_id=request.user.id, status='cart').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(cart, many=True)
        return Response(serializer.data)

    # редактировать корзину
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({'order': cart.id})
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError as error:
                            return JsonResponse({'Status': False, 'Errors': str(error)})
                        else:
                            objects_created += 1
                    else:
                        JsonResponse({'Status': False, 'Errors': serializer.errors})

                return JsonResponse({'Status': True, 'Создано объектов': objects_created})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить товары из корзины
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=cart.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # добавить позиции в корзину
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
                objects_updated = 0
                for order_item in items_dict:
                    if type(order_item['id']) == int and type(order_item['quantity']) == int:
                        objects_updated += OrderItem.objects.filter(order_id=cart.id, id=order_item['id']).update(
                            quantity=order_item['quantity'])

                return JsonResponse({'Status': True, 'Обновлено объектов': objects_updated})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class OrderView(APIView):
    """
    Класс для получения и размешения заказов пользователями
    """
    throttle_scope = 'user'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        order = Order.objects.filter(
            user_id=request.user.id).exclude(status='basket').select_related('contact').prefetch_related(
            'ordered_items').annotate(
            total_quantity=Sum('ordered_items__quantity'),
            total_sum=Sum('ordered_items__total_amount')).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    # Размещаем заказ из корзины и посылаем письмо об изменении статуса заказа.
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        if request.data['id'].isdigit():
            try:
                is_updated = Order.objects.filter(
                    id=request.data['id'], user_id=request.user.id).update(
                    contact_id=request.data['contact'],
                    status='new')
            except IntegrityError as error:
                return Response({'Status': False, 'Errors': 'Неправильно указаны аргументы'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if is_updated:
                    request.user.email_user(f'Обновление статуса заказа',
                                            'Заказ сформирован',
                                            from_email=settings.EMAIL_HOST_USER)
                    return Response({'Status': True})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'},
                        status=status.HTTP_400_BAD_REQUEST)


class PartnerOrders(APIView):
    """
    Класс для получения заказов поставщиками
    """
    throttle_scope = 'user'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Login required'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=status.HTTP_403_FORBIDDEN)

        pr = Prefetch('ordered_items', queryset=OrderItem.objects.filter(shop__user_id=request.user.id))
        order = Order.objects.filter(
            ordered_items__shop__user_id=request.user.id).exclude(status='basket') \
            .prefetch_related(pr).select_related('contact').annotate(
            total_sum=Sum('ordered_items__total_amount'),
            total_quantity=Sum('ordered_items__quantity'))

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)




class PartnerState(APIView):
    """
    Класс для работы со статусом поставщика
    """
    throttle_scope = 'user'

    # Получить текущий статус получения заказов у магазина
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Login required'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=status.HTTP_403_FORBIDDEN)

        shop = request.user.shop
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    # Изменить текущий статус получения заказов у магазина
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=status.HTTP_403_FORBIDDEN)

        state = request.data.get('state')
        if state:
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
                return Response({'Status': True})
            except ValueError as error:
                return Response({'Status': False, 'Errors': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Status': False, 'Errors': 'Не указан аргумент state.'}, status=status.HTTP_400_BAD_REQUEST)

# class CartViewSet(viewsets.ModelViewSet):
#
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()
#
#
#     @staticmethod
#     def get_cart(user):
#         if user.is_authenticated:
#             return Cart.objects.filter(owner=user.customer, for_anonymus_user=False).first()
#         return Cart.objects.filter(for_anonymus_user=True).first()
#
#
#     @staticmethod
#     def get_or_create_cp(customer: Customer, cart: Cart, product: Product):
#         cart_product, created = CartProduct.objects.get_or_create(
#             user=customer,
#             product=product,
#             cart=cart
#         )
#         return cart_product, created
#
#     @action(methods=['get'], detail=False)
#     def current_customer_cart(self, *args, **kwargs):
#         cart = self.get_cart(self.request.user)
#         cart_serializer = CartSerializer(cart)
#         return response.Response(cart_serializer.data)
#
#
#     @action(methods=["put"], detail=False, url_path='current_customer_cart/add_to_cart/(?P<product_id>\d+)')
#     def add_to_cart(self, *args, **kwargs):
#         cart = self.get_cart(self.request.user)
#         product = get_object_or_404(Product, id=kwargs['product_id'])
#         cart_product, created = self.get_or_create_cp(self.request.user.customer, cart, product)
#         if created:
#             cart.products.add(cart_product)
#             cart.save()
#             return response.Response({'detail': 'Товар добавлен в корзину'})
#         return response.Response({'detail': 'Товар уже в корзине'}, status=status.HTTP_400_BAD_REQUEST)
#
#
#     @action(methods=['path'], detail=False, url_path='current_customer_cart/change_qty/(?P<qty>\d+)/(?P<cart_product_id>\d+)')
#     def product_change_qty(self, *args, **kwargs):
#         cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
#         cart_product.qty = int(kwargs['qty'])
#         cart_product.save()
#         cart_product.cart.save()
#         return response.Response(status=status.HTTP_200_OK)
#
#
#     @action(methods=['put'], detail=False,
#             url_path='current_customer_cart/remove_from_cart/(?P<cart_product_id>\d+)')
#     def product_remove_from_cart(self, *args, **kwargs):
#         cart = self.get_cart(self.request.user)
#         cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
#         cart_products.remove(cart_product)
#         cart_product.delete()
#         cart.save()
#         return response.Response(status=status.HTTP_204_NO_CONTENT)