from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from alarms.models import Alarm
from alarms.permissions import IsOwner
from alarms.serializers import AlarmSerializer, UserSerializer


class AlarmListAPIView(generics.ListAPIView):
    queryset = Alarm.objects.order_by('-time')
    serializer_class = AlarmSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # def get_queryset(self):
    #     assert self.queryset is not None, (
    #             "'%s' should either include a `queryset` attribute, "
    #             "or override the `get_queryset()` method."
    #             % self.__class__.__name__
    #     )
    #
    #     queryset = self.queryset
    #     try:
    #         queryset = queryset.filter(owner=self.request.user)
    #     except TypeError:
    #         queryset = None
    #     return queryset


class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AlarmCRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    permission_classes = (IsOwner,)


@api_view(['POST'])
def create_alarm(request):
    data = request.data
    serializer = AlarmSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


