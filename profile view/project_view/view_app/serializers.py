from rest_framework import serializers
from .models import CustomUser,Imagemodel
 
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
 
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}
 
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
class ImagemodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagemodel
        fields = ['id','project_name','project_image','project_location','uploaded_by','project_start_date','project_end_date','people_working']
        