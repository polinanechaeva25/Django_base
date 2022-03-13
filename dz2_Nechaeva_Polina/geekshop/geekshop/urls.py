from django.urls import path
from mainapp import views as mainapp_views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('', mainapp_views.index, name='index'),
    path('contact/', mainapp_views.contact, name='contact'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('cart/', include('cartapp.urls', namespace='cart')),
    path('admin/', include('adminapp.urls', namespace='admin'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
