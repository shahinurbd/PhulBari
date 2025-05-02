from django.shortcuts import render
from rest_framework.viewsets import  ModelViewSet
from .serializers import OrderSerializer,UpdateOrderSerializer
from .models import Order
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class OrderViewSet(ModelViewSet):
    """
    Retrive all the orders.
    """
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    
    @action(detail=True, methods=['patch'], url_path='update')
    @swagger_auto_schema(
        operation_description="Update an existing Order status (Admin only)",
        responses={201: UpdateOrderSerializer()},
    )
    def update_status(self,request,pk=None, *args, **kwargs):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if order.status == 'Confirmed':
            if request.user.email:
                send_mail(
                    subject='Order Confirmed',
                    message=f'Hi {request.user.first_name}! Your order #{request.order.id} has been confirmed!\n Thank You.',
                    from_email='shahinurislam728@gmail.com',
                    recipient_list=[request.user.email],
                    fail_silently=False
                )
        
        return Response({
            "status": f"Order status updated to {request.data['status']}"
        })
    

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_serializer_class(self):
        if self.action == 'update_status':
            return UpdateOrderSerializer
        return OrderSerializer
    

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
