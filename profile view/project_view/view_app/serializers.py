from rest_framework import serializers
from .models import CustomUser,Projectmodel,MaterialModel
from .models import Worker,TaskModel

 
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
    
class ProjectmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projectmodel
        fields = ['id','project_name','project_image','project_location','uploaded_by','project_start_date','project_end_date','people_working']




class MaterialModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = ['id', 'material_type', 'total_quantity', 'quantity_used', 'quantity_left', 'arrival_date']
        read_only_fields = ['quantity_left']  # Make quantity_left read-only since it's auto-calculated

    def validate_quantity_used(self, value):
        """
        Ensure that quantity_used does not exceed total_quantity.
        """
        total_quantity = self.initial_data.get('total_quantity')
        if total_quantity is not None and value > int(total_quantity):
            raise serializers.ValidationError("Quantity used cannot exceed total quantity.")
        return value
    

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name', 'job_title','is_working','worker_id']
               

class TaskSerializer(serializers.ModelSerializer):
    worker = serializers.ListField(child=serializers.CharField(), write_only=True)
    
    class Meta:
        model = TaskModel
        fields = '__all__'

    def create(self, validate_data):
        workers_data = validate_data.pop('worker', [])
        task = TaskModel.objects.create(**validate_data)

        for worker_id in workers_data:
            try:
                worker = Worker.objects.get(worker_id=worker_id)
                if not worker.is_working:
                    task.worker.add(worker)
                    worker.is_working = True
                    worker.save()
                else:
                    raise serializers.ValidationError(f"Worker with ID {worker_id} is already working")
            except Worker.DoesNotExist:
                raise serializers.ValidationError(f"Worker with ID {worker_id} does not exist")

        return task


