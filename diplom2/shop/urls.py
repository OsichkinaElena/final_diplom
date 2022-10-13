from django.urls import path
from shop.views import PartnerUpdate

urlpatterns = [

    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),

]