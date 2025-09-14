from django.urls import path, include
from rest_framework.routers import DefaultRouter
from flowers.views import FlowerViewSet,FlowerImageViewSet,CategoryViewSet
from rest_framework_nested import routers
from orders.views import OrderViewSet
from users.views import AddressViewSet

router = routers.DefaultRouter()

router.register('flowers', FlowerViewSet, basename='flower')
router.register('categories', CategoryViewSet)
router.register('orders', OrderViewSet, basename='orders')
router.register('address', AddressViewSet, basename='address')



flower_router = routers.NestedDefaultRouter(router, 'flowers', lookup='flower')
flower_router.register('images', FlowerImageViewSet, basename='flower-image')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(flower_router.urls)),
    path('admin-dashboard/', include('admin_dashboard.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
