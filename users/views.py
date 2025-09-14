from rest_framework.viewsets import ModelViewSet
from .models import UserAddress
from .serializers import UserAddressSerializer

class AddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.prefetch_related('user_address').all()
    serializer_class = UserAddressSerializer

