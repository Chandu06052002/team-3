from rest_framework import serializers
from .models import CustomUser,Imagemodel,Cementmodel,Sandmodel,Bricksmodel,Gravelmodel
from .models import Worker

 
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



class CementmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cementmodel
        fields = ['id','total_bags','no_of_bags_used','no_of_bags_left','arrival_date']

class SandmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sandmodel
        fields = ['id','Total_trucks','no_of_trucks_used','no_of_trucks_left','trucks_arrival_date']

class BricksmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bricksmodel
        fields = ['id','Total_bricks','no_of_bricks_used','no_of_bricks_left','bricks_arrival_date']

class GravelmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gravelmodel
        fields = ['id','Total_trucks_of_gravel','no_of_trucks_used','no_of_trucks_left','trucks_arrival_date']

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name', 'job_title']
               

