from django.urls import path, include
from rest_framework.routers import DefaultRouter
from flowers.views import FlowerViewSet
from rest_framework_nested import routers
from orders.views import OrderViewSet

router = routers.DefaultRouter()


router.register('flowers', FlowerViewSet, basename='flower')

router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]
