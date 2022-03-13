from django.urls import path

from . import views

app_name = 'authapp'

urlpatterns = [
   path('login/', views.login, name='login'),
   path('logout', views.logout, name='logout'),
   path('edit', views.edit, name='edit'),
   path('register', views.register, name='register'),
]