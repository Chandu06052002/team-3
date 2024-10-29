from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser,Imagemodel
from .serializers import RegisterSerializer, CustomUserSerializer,ImagemodelSerializer
from rest_framework.parsers import MultiPartParser,FormParser

 
class RegisterView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class LoginView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
 
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
 
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Delete the token to log out the user
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token does not exist."}, status=status.HTTP_400_BAD_REQUEST)    
        
class Imageupload(APIView):
    parser_classes = (MultiPartParser,FormParser)

    def post(self,request,*args,**kwargs):
        serializer = ImagemodelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    