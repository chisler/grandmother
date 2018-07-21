from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from subscription.serializers import SubscriptionSerializer
from .models import User
from subscription.models import Subscription
from .models import User
import datetime


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


from rest_framework import serializers
from rest_framework.validators import UniqueValidator



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


class TraderSerializer(serializers.Serializer):
    is_followed = serializers.SerializerMethodField()
    growth =  serializers.SerializerMethodField() # monthly growth in percentage

    def get_growth(self, obj):
        today = datetime.date.today()
        lastMonth = today - datetime.timedelta(days=30)
        
        date_balances = obj.date_balances.filter(date__gte=lastMonth).order_by('date')
        diff = date_balances.last().balance - date_balances.first().balance
        return diff

    def get_is_followed(self, obj):
        return False

    class Meta:
        fields = ('is_followed', 'growth')