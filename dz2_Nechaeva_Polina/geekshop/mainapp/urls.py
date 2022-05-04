from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.products, name='index'),
    path('category/<int:pk>/', cache_page(3600)(views.products), name='category'),
    path('category/<int:pk>/page/<int:page>/', views.products, name='page'),
    path('product/<int:pk>/', views.product, name='product'),

]



