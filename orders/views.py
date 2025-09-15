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
    settings = { 'store_id': 'phima68807e60df4da', 'store_pass': 'phima68807e60df4da@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn {order_id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address.address
    post_body['cus_city'] = user.address.city
    post_body['cus_country'] = user.address.country
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "E-commerce Products"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)
    
    if response.get('status') == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_502_BAD_GATEWAY)

    return Response(response)

@api_view(['POST'])
def payment_success(request):
    print(request.data)

    order_id = request.data.get("tran_id").split('_')[1]
    
    order = Order.objects.get(id=order_id)
    order.status = "Ready To Ship"
    order.save()
    html = f"""
    <html>
        <head>
            <script>
                window.location.href = "{main_settings.FRONTEND_URL}/api/dashboard/orders/";
            </script>
        </head>
        <body>
            Redirecting...
        </body>
    </html>
    """
    return HttpResponse(html)


@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/api/dashboard/orders/")


@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/api/dashboard/orders/")
