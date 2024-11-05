from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import (
    CustomUser,
    Imagemodel,
    Cementmodel,
    Sandmodel,
    Bricksmodel,
    Gravelmodel,
    )
from .serializers import (
    RegisterSerializer, 
    CustomUserSerializer,
    ImagemodelSerializer,
    CementmodelSerializer,
    SandmodelSerializer,
    BricksmodelSerializer,
    GravelmodelSerializer,
    )
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
    

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return Response({"msg":"The password you have entered is incorrect"},status=status.HTTP_400_BAD_REQUEST)
            
        if len(new_password) < 6:
            return Response({"msg":"password atleast 6 characters"},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()

        return Response({"success":"password updated sucessfully"},status=status.HTTP_200_OK)
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CementmodelSerializer, SandmodelSerializer, BricksmodelSerializer, GravelmodelSerializer

class ResourceView(APIView):
    def get_serializer_class(self, resource_type):
        """Return the serializer class based on the resource type."""
        if resource_type == 'cement':
            return CementmodelSerializer
        elif resource_type == 'sand':
            return SandmodelSerializer
        elif resource_type == 'bricks':
            return BricksmodelSerializer
        elif resource_type == 'gravel':
            return GravelmodelSerializer
        else:
            return None

    def post(self, request):
        # Check if the user is a supervisor
        if request.user.role != 'supervisor':
            return Response(
                {"detail": "Only supervisors can create resources."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the resource type from the request data
        resource_type = request.data.get('resource_type')
        serializer_class = self.get_serializer_class(resource_type)

        # If the resource type is invalid, return an error
        if serializer_class is None:
            return Response(
                {"detail": "Invalid resource type specified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize the serializer with the data
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        """Retrieve a specific resource by its primary key (pk)."""
        resource_type = request.query_params.get('resource_type')
        serializer_class = self.get_serializer_class(resource_type)

        if serializer_class is None:
            return Response(
                {"detail": "Invalid resource type specified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the specific model based on the serializer
        model_class = serializer_class.Meta.model
        try:
            resource = model_class.objects.get(pk=pk)
        except model_class.DoesNotExist:
            return Response(
                {"detail": "Resource not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the resource
        serializer = serializer_class(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)

        