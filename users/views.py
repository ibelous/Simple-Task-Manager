from .serializers import *
from rest_framework import generics
from rest_framework.permissions import *
from rest_framework import status
from rest_framework.response import Response


from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserRetrieveSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    # permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={"token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
