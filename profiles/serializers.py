from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from subscription.models import Subscription
from .models import User


class SubscriptionSerializer(serializers.ModelSerializer):
    total_money = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('user_followed_id', 'money_allocated', 'initial_ration', 'total_money', 'name')

    def get_total_money(self, obj):
        return obj.get_total_money()

    def get_name(self, obj):
        return obj.user_followed.profile.name


class UserProfileSerializer(serializers.Serializer):
    total_money = serializers.SerializerMethodField()
    start_money = serializers.SerializerMethodField()
    free_money = serializers.SerializerMethodField()
    subscription = SubscriptionSerializer(many=True)

    def get_total_money(self, obj):
        return obj.get_total_money()

    def get_start_money(self, obj):
        return obj.profile.initial_money

    def get_free_money(self, obj):
        return obj.profile.free_money

    class Meta:
        fields = ('total_money', 'start_money', 'subscription', 'free_money')