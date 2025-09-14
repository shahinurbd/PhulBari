from rest_framework import serializers
from .models import Order
from flowers.models import Flower
from users.models import User, UserAddress



class EmptySerializer(serializers.Serializer):
    pass

class SimpleFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ['id', 'name', 'price']

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'country', 'city', 'area', 'address', 'zip', 'note']
        ref_name = 'OrderAddressSerializer'

class UserSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone_number']
        ref_name = 'OrdersUserSerializer'

    
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderSerializer(serializers.ModelSerializer):
    flower = SimpleFlowerSerializer()
    user = UserSerializer()
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'flower', 'quantity']

        