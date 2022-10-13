from django.urls import path, include
from rest_framework import routers
from .views import CategoryView, ShopView, ProductInfoView

app_name = 'shop'

router = routers.SimpleRouter()
router.register(r'shops', ShopView)
router.register(r'categories', CategoryView)
router.register(r'products', ProductInfoView, basename='products')