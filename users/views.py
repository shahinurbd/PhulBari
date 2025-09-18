from rest_framework.viewsets import ModelViewSet
from .models import UserAddress
from .serializers import UserAddressSerializer
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.prefetch_related('user_address').all()
    serializer_class = UserAddressSerializer


class ContactFormView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        title = request.data.get("title")
        message = request.data.get("message")

        if not (name and email and message):
            return Response({"error": "Name, email and message are required"}, status=status.HTTP_400_BAD_REQUEST)

        subject = f"New Contact Form Message: {title or 'No Title'}"
        body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Title: {title}
        Message: {message}
        """

        try:
            send_mail(
                subject,
                body,
                email, 
                ["shahinurislam728@gmail.com"], 
                fail_silently=False,
            )
            return Response({"success": "Message sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
