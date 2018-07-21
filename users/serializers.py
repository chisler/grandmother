import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer
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


def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

class TraderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=256)

    is_followed = serializers.SerializerMethodField()
    month_growth =  serializers.SerializerMethodField() # monthly growth in percentage
    followers_count =  serializers.SerializerMethodField() # monthly growth in percentage

    def get_month_growth(self, obj):
        today = datetime.date.today()
        lastMonth = today - datetime.timedelta(days=30)
        
        date_balances = obj.date_balances.filter(date__gte=lastMonth).order_by('date')
        month_ago = date_balances.first().balance
        now = date_balances.last().balance

        diff = get_change(now, month_ago) #month_ago #now / (month_ago / 100)
        return diff

    def get_is_followed(self, obj):
        return False

    def get_followers_count(self, obj):
        return Subscription.objects.filter(user_followed=obj).count()

    class Meta:
        fields = ('id', 'is_followed', 'growth', )