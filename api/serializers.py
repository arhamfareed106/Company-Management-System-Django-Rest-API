from rest_framework import serializers
from .models import Company, Employee

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'  # Or list the fields you want to expose, e.g., ['id', 'name', 'location', 'type']

class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)  # Nested serializer to show company info
    
    class Meta:
        model = Employee
        fields = '__all__'  # Or list the fields you want to expose
