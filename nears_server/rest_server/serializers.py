from rest_framework import serializers
from .models import UserAuth, User, Staff, Device, Department, Cases, CallLogs, Messages, Modes, Types

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = [ 'email', 'phone_number', 'device_id','password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'date_of_birth', 'account', 'place_of_residence', 'ghana_card_number']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['staff_username', 'first_name', 'last_name','account', 'position']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['location_coordinate', 'location', 'type', 'user_id', 'name', 'status']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'name', 'created_on', 'updated_on']

class CasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cases
        fields = ['case_id', 'type', 'mode', 'case', 'user_id', 'status', 'resource_id', 'location', 'place', 'realtime_updates', 'received_by', 'created_on', 'updated_on']

class CallLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLogs
        fields = ['call_id', 'from_number', 'duration', 'received_by', 'case_id', 'created_on', 'updated_on']

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['message_id', 'from_number', 'message', 'type', 'received_by', 'case_id', 'created_on', 'updated_on']

class ModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modes
        fields = ['mode_id', 'name']

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = ['type_id', 'name']
        
        
        

# GET

class StaffSerializer_R(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['staff_id', 'staff_username', 'first_name', 'last_name','account', 'position', 'created_on']