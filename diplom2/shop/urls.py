from django.urls import path, include
from shop.views import PartnerUpdate
# from rest_framework import routers





urlpatterns = [

    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('', include('shop.router')),


]

