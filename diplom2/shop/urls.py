from django.urls import path
from shop.views import ProductInfoView, ProductListView

urlpatterns = [

    # path('', index, name='index'),
    path('', ProductListView.as_view()),
    path('product/<pk>/', ProductInfoView.as_view()),
    # path('cart/', cart, name='cart'),
    # path('category/<int:category_id>/', show_category, name='product_list_by_category'),
    # path('product/<slug:product_slug/>', show_product, name='product'),

]