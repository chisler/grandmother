import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer, DateBalanceSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=1, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')



class UserProfileSerializer(serializers.Serializer):
    total_money = serializers.SerializerMethodField()
    start_money = serializers.SerializerMethodField()
    free_money = serializers.SerializerMethodField()
    subscription = SubscriptionSerializer(many=True)

    def get_total_money(self, obj):
        return obj.get_total_money() + obj.free_money

    def get_start_money(self, obj):
        return obj.initial_money

    def get_free_money(self, obj):
        return obj.free_money

    class Meta:
        fields = ('total_money', 'start_money', 'subscription', 'free_money')
