from django.urls import path

from . import views

app_name = 'cartapp'

urlpatterns = [
   path('', views.cart, name='view'),
   path('add/<int:pk>', views.add_to_cart, name='add'),
   path('remove/<int:pk>', views.remove_from_cart, name='remove'),
   path('edit/<int:pk>/<int:quantity>/', views.cart_edit, name='edit'),

]