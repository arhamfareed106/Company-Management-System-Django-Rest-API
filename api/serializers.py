from rest_framework import serializers
from api.models import Company, Employee  # Ensure Employee model is imported

# Serializer for the Company model
class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

# Serializer for the Employee model
class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
