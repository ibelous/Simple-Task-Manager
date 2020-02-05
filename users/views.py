from .serializers import *
from rest_framework import generics, views
from .permissions import IsManager, IsOwnerOrManager
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import login, logout


from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserRetrieveUpdateDestroySerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserRetrieveUpdateDestroySerializer
    permission_classes = (IsManager, )
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRetrieveUpdateDestroySerializer
    lookup_field = 'pk'
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrManager, )


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response(
                data={"token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class Logout(views.APIView):
    def get(self, request):
        # simply delete the token to force a login
        logout(request)
        return Response(status=status.HTTP_200_OK)
