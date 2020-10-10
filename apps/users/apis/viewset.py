from rest_framework import viewsets, response, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.views import APIView

from apps.users.apis.serializers import TokenSerializer, UserSerializer, TokenCreateSerializer
from apps.users.models import User


class AuthLogInViewSet(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serializer_token = TokenCreateSerializer(token, context={'request': request})
        return response.Response(serializer_token.data)


class AuthLogOutViewSet(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return response.Response(data={'detail': 'bye'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        data = Token.objects.all()
        serializer = TokenCreateSerializer(data, many=True, context={'request': request})
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data_user = request.data
        serializer_user = UserSerializer(data=data_user)
        serializer_user.is_valid(raise_exception=True)
        username = serializer_user.save()
        data_token = Token.objects.filter(user__username=username).first()
        serializer_token = TokenSerializer(data_token, context={"request": request})
        return response.Response(serializer_token.data)

    @action(methods=['GET'], detail=False, url_path='(?P<user_id>[0-9]+)')
    def token_by_user(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        data = Token.objects.filter(user_id=user_id)
        if data.count() > 0:
            serializer = TokenSerializer(data.first(), context={"request": request})
            return response.Response(serializer.data)
        else:
            serializer = {'detail': 'This user not exist'}
            return response.Response(serializer)

    @action(methods=['GET'], detail=False, url_path='is_login')
    def is_login(self, request, *args, **kwargs):
        token = request.user.auth_token
        data = Token.objects.filter(key=token)
        if data.count() > 0:
            serializer = TokenSerializer(data.first(), context={"request": request})
            return response.Response(serializer.data)
        else:
            serializer = {'detail': 'This user not login'}
            return response.Response(serializer)
