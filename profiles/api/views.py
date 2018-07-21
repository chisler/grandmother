from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import UserProfileSerializer
from users.models import User


class UserProfileGet(APIView):
    """ 
    Creates the user. 
    """

    def get(self, request, format='json'):
        serializer = UserProfileSerializer(User.objects.get(id=2))
        return Response(data=serializer.data)

