from rest_framework import serializers
from .models import Company, Employee, Project

class CompanySerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'location', 'type', 'website', 
            'established_date', 'description', 'slug',
            'employee_count', 'project_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_employee_count(self, obj):
        return obj.employee_set.count()

    def get_project_count(self, obj):
        return obj.project_set.count()

class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'email', 'phone', 'position',
            'company', 'company_name', 'hire_date', 'salary',
            'is_active', 'project_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_project_count(self, obj):
        return obj.projects.count()

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value

class ProjectSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'company', 'company_name',
            'employees', 'start_date', 'end_date', 'status',
            'budget', 'employee_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_employee_count(self, obj):
        return obj.employees.count()

    def validate(self, data):
        if data.get('end_date') and data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })
        return data
