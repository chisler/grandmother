import datetime

from rest_framework import serializers

from external.exchange_api import ExternalExchange
from django.conf import settings

from gettingstarted import followtask
from subscription.models import Subscription, DateBalance, CurrencyBalance


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
        fields = ('date', 'balance',)



class TraderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=256)
    name = serializers.SerializerMethodField()

    subscription_id = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    month_growth = serializers.SerializerMethodField()  # monthly growth in percentage
    followers_count = serializers.SerializerMethodField()
    date_balances = DateBalanceSerializer(many=True)

    def get_name(self, obj):
        return obj.name

    def get_month_growth(self, obj):
        today = datetime.date.today()
        lastMonth = today - datetime.timedelta(days=30)

        date_balances = obj.date_balances.filter(date__gte=lastMonth).order_by('date')
        month_ago = date_balances.first().balance
        now = date_balances.last().balance

        diff = get_change(now, month_ago)  # month_ago #now / (month_ago / 100)
        return diff

    def get_subscription_id(self, obj):
        sub = Subscription.objects.filter(follower_id=settings.SAMPLE_USER, user_followed=obj.id)
        if sub:
            return sub.first().id

        return None

    def get_is_followed(self, obj):
        return Subscription.objects.filter(follower_id=settings.SAMPLE_USER, user_followed=obj.id).exists()

    def get_followers_count(self, obj):
        return Subscription.objects.filter(user_followed=obj).count()

    class Meta:
        fields = ('id', 'is_followed', 'growth', 'data_balances')

class SubscriptionSerializer(serializers.ModelSerializer):
    total_money = serializers.SerializerMethodField()
    trader = TraderSerializer(source='user_followed')
    name = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'user_followed_id', 'money_allocated', 'initial_ratio', 'total_money', 'trader', 'name')

    def get_name(self, obj):
        return obj.user_followed.name

    def get_total_money(self, obj):
        return obj.get_total_money()

def _create_orders(trader_wallets, initial_ratio, investor):
    investor_exchange = ExternalExchange(api_key=investor.api_key, secret_key=investor.secret_key)

    # if 'BTC' in trader_wallets:
    #     # workaround with addition transaction due to absence of more cryptopairs on ethfinex
    #     amount = trader_wallets['BTC']
    #     price_eth_in_btc = investor_exchange.market_order_buy('ETH/BTC', amount * initial_ratio)
    #     eth_amount = amount * initial_ratio / price_eth_in_btc
    #     investor_exchange.market_order_sell('ETH/USDT', eth_amount * 0.95)  # fee
    #     trader_wallets.pop('BTC')
    trader_wallets.pop('USDT') # do not trade with USDT
    orders = [{'currency': currency + '/USDT', 'amount': amount * initial_ratio} for (currency, amount) in trader_wallets.items()]
    investor_exchange.batch_market_buy(orders)


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('follower', 'user_followed', 'money_allocated')

    def create(self, validated_data):

        trader = validated_data['user_followed']
        investor = validated_data['follower']

        trader_money = trader.get_total_money()
        money_allocated = validated_data['money_allocated'] # to be sure that we will have enough money

        if not settings.MODE and len(trader.api_key) > 5:
            followtask.start_web_socket.delay(trader.id)
            trader_exchange = ExternalExchange(api_key=trader.api_key, secret_key=trader.secret_key)
            trader_wallets = trader_exchange.get_user_wallets()
            trader_money = trader_exchange.get_usd_balance_from_wallets(trader_wallets)

        investor.free_money -= validated_data['money_allocated']
        investor.save()

        initial_ratio = money_allocated / (trader_money or 1)

        if not settings.MODE and len(trader.api_key) > 5:
            _create_orders(trader_wallets, initial_ratio, investor)

        validated_data['initial_ratio'] = initial_ratio
        return super().create(validated_data)

        # return instance

