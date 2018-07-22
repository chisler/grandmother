from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from subscription.models import Subscription, CurrencyBalance
from subscription.serializers import SubscriptionCreateSerializer


class SubscribeAPI(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = SubscriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            CurrencyBalance.objects.create(subscription=instance, name='USD', amount=instance.money_allocated)
            json = serializer.data
            return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnsubscribeAPI(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, subscription_id, format='json'):

        s = Subscription.objects.get(id=subscription_id)
        print('HEY')
        total_money = s.get_total_money()
        s.follower.free_money += total_money
        s.follower.save()
        s.delete()

        return Response(status=status.HTTP_201_CREATED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)