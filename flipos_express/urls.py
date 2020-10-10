"""flipos_express URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers

from apps.orders.apis.viewset import OrderViewSet
from apps.users.apis.viewset import AuthLogInViewSet, AuthLogOutViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/login', AuthLogInViewSet.as_view()),
    path('api-auth/logout', AuthLogOutViewSet.as_view()),
]
