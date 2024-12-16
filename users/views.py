

from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework import status
from users.tokens import create_jwt_pair_for_user
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated 

class ListCreateUser(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            success_response = {
                "status": status.HTTP_201_CREATED,
                "message": "User created successfully"
            }
            return Response(success_response, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request: Request):
        numero_de_telephone = request.data.get("numero_de_telephone")
        password = request.data.get("password")
        print(numero_de_telephone,password)
        user = authenticate(numero_de_telephone=numero_de_telephone, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Succesfull", "token": tokens}#,"id":user.id
            return Response(data=response, status=status.HTTP_200_OK)
        

        else:
            error_response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "errorMessage": "Invalid email or password"
            }
            return Response(data=error_response, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class RetrieveUser(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

