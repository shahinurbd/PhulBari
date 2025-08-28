from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from orders.serializers import OrderSerializer

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']


class UserSerializer(BaseUserSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUser"
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'orders', 'is_staff']
        read_only_fields = ['is_staff']
    
