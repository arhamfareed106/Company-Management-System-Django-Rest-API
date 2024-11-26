from rest_framework import serializers
from .models import Company, Employee, Project

class CompanySerializer(serializers.ModelSerializer):
    company_id= serializers.ReadOnlyField()
    employee_count = serializers.SerializerMethodField()
    active_projects = serializers.SerializerMethodField()
    department_distribution = serializers.SerializerMethodField()
    total_salary_expense = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'
        extra_fields = ['employee_count', 'active_projects', 'department_distribution', 'total_salary_expense']

    def get_employee_count(self, obj):
        return obj.employee_set.count()

    def get_active_projects(self, obj):
        return obj.project_set.exclude(status='COMP').count()

    def get_department_distribution(self, obj):
        return obj.get_department_distribution()

    def get_total_salary_expense(self, obj):
        return sum(employee.salary for employee in obj.employee_set.all())

class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    experience_years = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'
        extra_fields = ['experience_years', 'company_name', 'project_count']

    def get_experience_years(self, obj):
        return obj.calculate_experience()

    def get_company_name(self, obj):
        return obj.company.name

    def get_project_count(self, obj):
        return obj.projects.count()

class ProjectSerializer(serializers.ModelSerializer):
    team_size = serializers.SerializerMethodField()
    duration_days = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['team_size', 'duration_days', 'company_name']

    def get_team_size(self, obj):
        return obj.team_members.count()

    def get_duration_days(self, obj):
        return obj.get_duration()

    def get_company_name(self, obj):
        return obj.company.name
