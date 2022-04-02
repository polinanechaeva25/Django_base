from django.urls import path
from ordersapp.views import OrderListView, OrderCreateView, OrderItemsUpdateView, OrderDeleteView, OrderDetailView\
    , order_forming_complete

app_name = "ordersapp"

urlpatterns = [
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderItemsUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]


