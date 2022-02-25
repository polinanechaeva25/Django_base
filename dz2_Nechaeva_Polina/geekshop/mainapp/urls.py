from django.urls import path

from . import views

app_name = 'mainapp'

urlpatterns = [
   path('', views.products, name='index'),
   path('<int:pk>/', views.products, name='category'),
]


