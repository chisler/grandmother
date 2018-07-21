from rest_framework import serializers

from subscription.models import Subscription, DateBalance
from users.models import User


class DateBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateBalance
        fields = ('date', 'balance', )


class SubscriptionSerializer(serializers.ModelSerializer):
    total_money = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('user_followed_id', 'money_allocated', 'initial_ratio', 'total_money', 'name')

    def get_total_money(self, obj):
        return obj.get_total_money()

    def get_name(self, obj):
        return obj.user_followed.username


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('follower', 'user_followed', 'money_allocated')

    def create(self, validated_data):
        trader_money = User.objects.get(id=validated_data['user_followed']).get_total_money()

        validated_data['initial_ratio'] = validated_data['money_allocated'] / trader_money
        return super().create(validated_data)

