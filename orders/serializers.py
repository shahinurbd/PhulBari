from rest_framework import serializers
from .models import Order
from flowers.models import Flower



class EmptySerializer(serializers.Serializer):
    pass

class SimpleFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ['id', 'name', 'price']

    
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderSerializer(serializers.ModelSerializer):
    flower = SimpleFlowerSerializer()
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'flower', 'quantity']

        