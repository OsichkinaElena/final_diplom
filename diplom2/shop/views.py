from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductInfo
from rest_framework.generics import ListAPIView, RetrieveAPIView
from shop.serializers import ProductListSerializer


class ProductInfoView(RetrieveAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductListSerializer
    filterset_fields = ['shop', 'price']


class ProductListView(ListAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductListSerializer
    filterset_fields = ['shop', 'price']




def authorization(request):

    return HttpResponse('авторизация')



def cart(request):

    return HttpResponse('корзина')


def show_category(request, category_id):
    product = Product.objects.filter(category_id=category_id)

    if len(product) == 0:
        raise Http404()

    context = {
        'product': product,
        'menu': menu,
        'title': 'Отображение по категориям',
        'cat_selected': category_id,
    }

    return render(request, 'shop/index.html', context=context)
