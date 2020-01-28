from django.urls import path
from . import views
from shop.views import ProdList, CategoryProductVue

app_name = 'shop'

urlpatterns = [
    path('', ProdList.as_view(), name='product_list_url'),
    # path('', CategoryProductVue.as_view(), name='product_list_url'),
]