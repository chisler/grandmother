import datetime

from rest_framework import serializers

from subscription.models import Subscription, DateBalance
from users.models import User

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


class DateBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateBalance
        fields = ('date', 'balance', )



class TraderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=256)

    is_followed = serializers.SerializerMethodField()
    month_growth = serializers.SerializerMethodField()  # monthly growth in percentage
    followers_count = serializers.SerializerMethodField()
    date_balances = DateBalanceSerializer(many=True)

    def get_month_growth(self, obj):
        today = datetime.date.today()
        lastMonth = today - datetime.timedelta(days=30)

        date_balances = obj.date_balances.filter(date__gte=lastMonth).order_by('date')
        month_ago = date_balances.first().balance
        now = date_balances.last().balance

        diff = get_change(now, month_ago)  # month_ago #now / (month_ago / 100)
        return diff

    def get_is_followed(self, obj):
        return False

    def get_followers_count(self, obj):
        return Subscription.objects.filter(user_followed=obj).count()

    class Meta:
        fields = ('id', 'is_followed', 'growth', 'data_balances')

class SubscriptionSerializer(serializers.ModelSerializer):
    total_money = serializers.SerializerMethodField()
    trader = TraderSerializer(source='user_followed')

    class Meta:
        model = Subscription
        fields = ('user_followed_id', 'money_allocated', 'initial_ratio', 'total_money', 'trader')

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

