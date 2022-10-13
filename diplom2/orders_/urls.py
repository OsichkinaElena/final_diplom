
from django.urls import path, include, re_path
from .views import PartnerState, CartView, OrderView

urlpatterns = [
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('cart', CartView.as_view(), name='cart'),
    path('order', OrderView.as_view(), name='order'),

]