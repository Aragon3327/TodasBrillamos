from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            user = Usuario.objects.get(email = request.data['username'])
        except:
            return Response(status = status.HTTP_406_NOT_ACCEPTABLE)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'userId': user.pk,
            })
        except:
            return Response(status = status.HTTP_401_UNAUTHORIZED)