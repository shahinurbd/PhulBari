from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from rest_framework.viewsets import ModelViewSet
from .serializers import OrderSerializer, UpdateOrderSerializer
from .models import Order
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings as main_settings
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework import status




class OrderViewSet(ModelViewSet):
    """
    Retrieve all the orders.
    """
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['patch'], url_path='update')
    @swagger_auto_schema(
        operation_description="Update an existing Order status (Admin only)",
        responses={201: UpdateOrderSerializer}, 
    )
    def update_status(self, request, pk=None, *args, **kwargs):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if order.status == 'Confirmed':
            if request.user.is_authenticated and request.user.email:
                send_mail(
                    subject='Order Confirmed',
                    message=f'Hi {request.user.first_name}! Your order #{order.id} has been confirmed!\n Thank You.',
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
        user = self.request.user
        return {
            'user_id': user.id if user and user.is_authenticated else None, 
            'user': user if user and user.is_authenticated else None
        }

    def get_serializer_class(self):
        if self.action == 'update_status':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Order.objects.none()
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    

@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    order_id = request.data.get("OrderId") 

    settings = { 
        'store_id': 'phulb68cadde9d25f9', 
        'store_pass': 'phulb68cadde9d25f9@ssl', 
        'issandbox': True 
    }
    sslcz = SSLCOMMERZ(settings)

    post_body = {
        'total_amount': amount,
        'currency': "BDT",
        'tran_id': f"txn_{order_id}",
        'success_url': f"{main_settings.BACKEND_URL}/api/payment/success/",
        'fail_url': f"{main_settings.BACKEND_URL}/api/payment/fail/",
        'cancel_url': f"{main_settings.BACKEND_URL}/api/payment/cancel/",
        'emi_option': 0,
        'cus_name': f"{user.first_name} {user.last_name}",
        'cus_email': user.email,
        'cus_phone': user.phone_number,
        'cus_add1': user.address.address,
        'cus_city': user.address.city,
        'cus_country': user.address.country,
        'shipping_method': "NO",
        'num_of_item': 1,
        'product_name': "E-commerce Products",
        'product_category': "General",
        'product_profile': "general",
        'value_a': f"{main_settings.FRONTEND_URL}/dashboard/orders/"
    }

    response = sslcz.createSession(post_body)
    
    if response.get('status') == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_502_BAD_GATEWAY)


@api_view(['POST'])
def payment_success(request):
    tran_id = request.data.get("tran_id")
    if not tran_id:
        return HttpResponse("Invalid response from SSLCommerz", status=400)

    try:
        order_id = tran_id.split('_')[1]
    except IndexError:
        return HttpResponse("Invalid transaction ID format", status=400)

    order = Order.objects.filter(id=order_id).first()
    if not order:
        return HttpResponse("Order not found", status=404)

    
    order.status = "Ready To Ship"
    order.save()

    
    frontend_redirect = request.data.get("value_a", f"{main_settings.FRONTEND_URL}/")
    return HttpResponseRedirect(frontend_redirect)


@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")


@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")
