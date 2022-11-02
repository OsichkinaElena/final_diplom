from django.db.models import Q, Sum, F
from .models import Category, Product, ProductInfo, Shop
# from rest_framework.generics import ListAPIView, RetrieveAPIView
from shop.serializers import ProductInfoSerializer, ShopSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.views import APIView


class CategoryView(viewsets.ModelViewSet):
    """
    Класс для просмотра категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering = ('name',)


class ShopView(viewsets.ModelViewSet):
    """
    Класс для просмотра списка магазинов
    """

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    ordering = ('name',)


class ProductInfoView(viewsets.ReadOnlyModelViewSet):
    """
    Класс для поиска товаров
    """
    throttle_scope = 'anon'
    serializer_class = ProductInfoSerializer
    ordering = ('product',)

    def get_queryset(self):

        query = Q(shop__state=True)
        shop_id = self.request.query_params.get('shop_id')
        category_id = self.request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()

        return queryset



class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """
    throttle_scope = 'partner'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES
        if file:
            user_id = request.user.id
            import_shop_data(file, user_id)

            return Response({'Status': True})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'},
                        status=status.HTTP_400_BAD_REQUEST)
