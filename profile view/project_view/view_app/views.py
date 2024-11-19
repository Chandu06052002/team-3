from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import (
    CustomUser,
    Projectmodel,
    MaterialModel,
    )
from .serializers import (
    RegisterSerializer, 
    CustomUserSerializer,
    ProjectmodelSerializer,
    MaterialModelSerializer,
    )
from rest_framework.parsers import MultiPartParser,FormParser
from .models import Worker
from .serializers import WorkerSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# REGISTER DATA
 
class RegisterView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(({'token': token.key},{"msg":"User registered successfully"}),status=status.HTTP_201_CREATED)
        return Response((serializer.errors,{"msg":"please provide valid details"}), status=status.HTTP_400_BAD_REQUEST)
 
# LOGIN DATA

class LoginView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
 
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(({'token': token.key},{"msg":"User login successfully"}), status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
 
# USER DETAILS DATA

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response((serializer.data,{"msg":"User details fetched successfully"}),status=status.HTTP_200_OK)
    
# LOGOUT DATA 
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Delete the token to log out the user
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token does not exist."}, status=status.HTTP_400_BAD_REQUEST)    

# IMAGEFIELD DATA

class Projectupload(APIView):
    parser_classes = (MultiPartParser,FormParser)

    def post(self,request,*args,**kwargs):
        serializer = ProjectmodelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response((serializer.data,{"msg":"details uploaded successfully"}),status=status.HTTP_201_CREATED)
        return Response((serializer.errors,{"msg":"please provide valid details"}),status=status.HTTP_400_BAD_REQUEST)
    
# PASSWORD CHANGE DATA

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


#RESOURCE DATA

@method_decorator(csrf_exempt, name='dispatch')
class ResourceView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Check if the user has a supervisor role
            if not hasattr(request.user, 'role') or request.user.role.lower() != 'supervisor':
                return JsonResponse(
                    {'error': 'Only supervisors can add materials'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Parse JSON data
            data = json.loads(request.body)
            material_type = data.get('material_type')
            total_quantity = data.get('total_quantity')
            quantity_used = data.get('quantity_used')
            arrival_date = data.get('arrival_date')

            # Validate that required fields are provided
            if not all([material_type, total_quantity, quantity_used, arrival_date]):
                return JsonResponse({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new MaterialModel object
            material = MaterialModel(
                material_type=material_type,
                total_quantity=total_quantity,
                quantity_used=quantity_used,
                arrival_date=arrival_date
            )
            material.save()

            # Prepare response data
            response_data = {
                'message': 'Material added successfully',
                'data': {
                    'id': material.id,
                    'material_type': material.material_type,
                    'total_quantity': material.total_quantity,
                    'quantity_used': material.quantity_used,
                    'quantity_left': material.quantity_left,
                    'arrival_date': material.arrival_date
                }
            }

            return JsonResponse(response_data, status=status.HTTP_201_CREATED)
        
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any other unexpected errors
            return JsonResponse({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# WORKERS DATA

class AddWorkerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'supervisor':
            return Response({"detail": "You do not have permission to add workers."}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            # Set the hired_by field to the current user
            worker = serializer.save(hired_by=request.user)  # This sets hired_by automatically
            return Response((serializer.data,{"msg":"worker created successfully"}), status=status.HTTP_201_CREATED)
        return Response((serializer.errors,{"msg":"please provide required details"}), status=status.HTTP_400_BAD_REQUEST)
