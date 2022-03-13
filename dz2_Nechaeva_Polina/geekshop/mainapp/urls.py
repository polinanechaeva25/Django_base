from django.urls import path

from . import views

app_name = 'mainapp'

urlpatterns = [
   path('', views.products, name='index'),
   path('category/<int:pk>/', views.products, name='category'),
   path('product/<int:pk>/', views.product, name='product'),
]


