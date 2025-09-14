from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from orders.serializers import OrderSerializer
from rest_framework import serializers
from .models import UserAddress


User = get_user_model()

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'country', 'city', 'area', 'address', 'zip', 'note']

class UserCreateSerializer(BaseUserCreateSerializer):
    address = UserAddressSerializer(required=False)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']

    def create(self, validated_data):
        address_data = validated_data.pop("address", None)
        user = super().create(validated_data)

        if address_data:
            address = UserAddress.objects.create(**address_data)
            user.address = address
            user.save()

        return user


class UserSerializer(BaseUserSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    address = UserAddressSerializer(required=False)
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUser"
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'orders', 'is_staff']
        read_only_fields = ['is_staff']


    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)

    
        instance = super().update(instance, validated_data)

        
        if address_data:
            if instance.address:
                for field, value in address_data.items():
                    setattr(instance.address, field, value)
                instance.address.save()
            else:
                address = UserAddress.objects.create(**address_data)
                instance.address = address
                instance.save()

        return instance
    
