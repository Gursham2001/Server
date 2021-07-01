from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers import UserSerializer
from .populated import PopulatedUserSerializer

User = get_user_model()
class RegisterView(APIView):

    def post(self, request):
        print(request.data)
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {'message: Registration Successfull'},
                status=status.HTTP_201_CREATED
            )
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'Unauthorized'})

        if not user_to_login.check_password(password):
            raise PermissionDenied({'detail': 'Unauthorized'})

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': user_to_login.id, 'exp':  int(expiry_time.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response(
            {'token': token, 'message': f'Welcome back {user_to_login.username}'}
        )

class ProfileDetailView(APIView):
    def get(self, _request, pk):
        try:
            user = User.objects.get(pk=pk)
            serialized_user = PopulatedUserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound()

    def put(self, request, pk):
        request.data['owner'] = request.user.id
        user_to_update = User.objects.get(pk=pk)
        updated_user = UserSerializer(user_to_update, data=request.data)
        if updated_user.is_valid():
            updated_user.save()
            return Response(updated_user.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_user.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileView(APIView):
    def get(self, _request):
        user = User.objects.all()
        serialized_user = PopulatedUserSerializer(user, many=True)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
