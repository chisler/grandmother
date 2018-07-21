from rest_framework import serializers

from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    total_money = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('user_followed_id', 'money_allocated', 'initial_ration', 'total_money', 'name')

    def get_total_money(self, obj):
        return obj.get_total_money()

    def get_name(self, obj):
        return obj.user_followed.username
