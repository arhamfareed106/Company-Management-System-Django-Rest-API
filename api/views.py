from argparse import Action
from multiprocessing import context
from django.views.generic import ListView, DetailView
from django.db.models import Q
from rest_framework import viewsets
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.paginator import Paginator

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    template_name = 'company_list.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Company.objects.all()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(type__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        try:   
            company = Company.objects.get(pk=pk)
            emps = Employee.objects.filter(company=company)
            emps_serializer = EmployeeSerializer(emps, many=True, context={'request': request})
            return Response(emps_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message': 'Company might not exist'
            })

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    template_name = 'employee_list.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Employee.objects.all()
        search = self.request.GET.get('search', '')
        position = self.request.GET.get('position', '')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__name__icontains=search)
            )
        
        if position:
            queryset = queryset.filter(position=position)
            
        return queryset.select_related('company')
