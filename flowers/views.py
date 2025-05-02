from django.shortcuts import render
from rest_framework.response import Response
from .models import Flower,FlowerImage,Category
from .serializers import FlowerSerializer,FlowerImageSerializer,CategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FlowerFilter
from .paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework import status
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class FlowerImageViewSet(ModelViewSet):
    """
    Retrive all the flowers images
    """
    serializer_class = FlowerImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return FlowerImage.objects.filter(flower_id=self.kwargs.get('flower_pk'))
    
    def perform_create(self, serializer):
        serializer.save(flower_id=self.kwargs.get('flower_pk'))
        

class FlowerViewSet(ModelViewSet):
    """
    Retrive a list of all the flowers
    """
    queryset = Flower.objects.prefetch_related('images').all()
    serializer_class = FlowerSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = FlowerFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    
    @action(detail=True, methods=['get','post'], url_path='buy', url_name='buy')
    @swagger_auto_schema(
        operation_description="Buy a Flower",
        responses={201: FlowerSerializer()},
    )
    def buy(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response({
                "error": "Please login first"
            })
        user = self.request.user
        flower = self.get_object()
        quantity = int(request.data.get('quantity', 1))

        if flower.stock < quantity:
            return Response({
                "error": "This Flower is out of stock."
            })
        order = Order.objects.create(user=user,flower=flower, quantity=quantity)
        flower.stock -= quantity
        flower.save()

        if request.user.email:
            send_mail(
                subject='Order Confirmation',
                message=f'Thank you {request.user.first_name}! You ordered {quantity} {flower.name}(s).',
                from_email='shahinurislam728@gmail.com',
                recipient_list=[request.user.email],
                fail_silently=False
            )


        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)



class CategoryViewSet(ModelViewSet):
    """
    Retrive a list of all the flowers category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]





