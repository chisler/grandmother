from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from subscription.serializers import TraderSerializer
from users.models import User
from users.serializers import UserSerializer, UserProfileSerializer


class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileGet(APIView):
    def get(self, request, user_id, format='json'):
        serializer = UserProfileSerializer(User.objects.get(id=user_id))
        return Response(data=serializer.data)


class GetTraders(APIView):
    """ 
    Get traders
    """
    def get(self, request, format='json'):
        traders = User.objects.filter(role=User.TRADER)
            # .annotate(is_followed=Count('book'))
            # .exclude(
            # id__in=Subscription.objects.filter(follower=user_id).values_list('user_followed_id', flat=True)
        # )

        serializer = TraderSerializer(traders, many=True)
        return Response(data=serializer.data)

