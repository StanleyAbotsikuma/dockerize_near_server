from rest_framework import viewsets, status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from django.http import Http404

from .models import User, Staff, Device, Department, Cases, CallLogs, Messages, Modes, Types,UserAuth
from .serializers import *

class UserAuthView(generics.ListCreateAPIView):
    queryset = UserAuth.objects.all()
    serializer_class = UserAuthSerializer
    def get(self, request, *args, **kwargs):
        # Raise a MethodNotAllowed exception for GET requests
        raise MethodNotAllowed(request.method)

    def post(self, request, *args, **kwargs):
        # Call the original post method to handle POST requests
        return super().post(request, *args, **kwargs)

@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)


class StaffViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        try:
           
            queryset = Staff.objects.get(account=user)
            serializer = StaffSerializer_R(queryset)
            return Response(serializer.data)
            
            
        except Staff.DoesNotExist:
            return Response({'error': 'Staff with id {} does not exist'.format(user)}, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        user = request.user
        try:
            if Staff.objects.get(account=user):
                return Response({'error': 'Staff with id {} already exist'.format(user)}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                (request.data).update({'account':user.id})
        except Staff.DoesNotExist:
            (request.data).update({'account':user.id})
            
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class CasesViewSet(viewsets.ModelViewSet):
    queryset = Cases.objects.all()
    serializer_class = CasesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class CallLogsViewSet(viewsets.ModelViewSet):
    queryset = CallLogs.objects.all()
    serializer_class = CallLogsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        # Clean and verify fields here using serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class ModesViewSet(viewsets.ModelViewSet):
    queryset = Modes.objects.all()
    serializer_class = ModesSerializer

@permission_classes([IsAuthenticated])
class TypesViewSet(viewsets.ModelViewSet):
    queryset = Types.objects.all()
    serializer_class = TypesSerializer
    
  