"""
URL configuration for lab_electiva project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.producto.api.ViewSets import ProductoViewSet, CategoriaViewSet
from apps.venta.api.ViewSets import VentaViewSet, RendicionDiariaViewSet

router_V1 = routers.DefaultRouter()
router_V1.register(prefix='producto',viewset=ProductoViewSet,basename='producto')
router_V1.register(prefix='categoria',viewset=CategoriaViewSet, basename='categoria')
router_V1.register(prefix='venta',viewset=VentaViewSet, basename='venta')
router_V1.register(prefix='cierre_de_caja',viewset=RendicionDiariaViewSet, basename='cierre_de_caja')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include(router_V1.urls)),
    path('api/v1/token/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('api/v1/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]
