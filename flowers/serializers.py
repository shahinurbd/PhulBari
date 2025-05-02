from rest_framework import serializers
from .models import Flower, Category, FlowerImage
from django.contrib.auth import get_user_model
from django.urls import reverse
from orders.models import Order

class FlowerImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = FlowerImage
        fields = ['id', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class FlowerSerializer(serializers.ModelSerializer):
    images = FlowerImageSerializer(many=True, read_only=True)
    Buy_Now = serializers.SerializerMethodField('get_buy_link')
    class Meta:
        model = Flower
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'images', 'Buy_Now']

    def get_buy_link(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'{obj.pk}/buy/')

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price could not be negative')
        return price
    

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()
    
