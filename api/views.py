from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .models import Company, Employee, Project
from .serializers import CompanySerializer, EmployeeSerializer
from django.db.models import Avg, Count
from django.utils import timezone
import json

class HomeView(TemplateView):
    template_name = 'home.html'

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

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

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return Response(
                {'companies': self.get_queryset()},
                template_name='company_list.html'
            )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.accepted_renderer.format == 'html':
            return Response(
                {'company': instance},
                template_name='company_detail.html'
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            if request.method == 'GET':
                return Response({'serializer': self.get_serializer()}, template_name='company_form.html')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'company': serializer.instance}, template_name='company_detail.html', status=status.HTTP_201_CREATED)
            return Response({'serializer': serializer}, template_name='company_form.html')
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        try:   
            company = self.get_object()
            emps = Employee.objects.filter(company=company)
            if request.accepted_renderer.format == 'html':
                return Response(
                    {'company': company, 'employees': emps},
                    template_name='company_detail.html'
                )
            emps_serializer = EmployeeSerializer(emps, many=True, context={'request': request})
            return Response(emps_serializer.data)
        except Exception as e:
            print(e)
            return Response({'message': 'Company might not exist'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

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

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return Response(
                {'employees': self.get_queryset()},
                template_name='employee_list.html'
            )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.accepted_renderer.format == 'html':
            return Response(
                {'employee': instance},
                template_name='employee_detail.html'
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            if request.method == 'GET':
                return Response({'serializer': self.get_serializer()}, template_name='employee_form.html')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'employee': serializer.instance}, template_name='employee_detail.html', status=status.HTTP_201_CREATED)
            return Response({'serializer': serializer}, template_name='employee_form.html')
        return super().create(request, *args, **kwargs)

class AnalyticsDashboardView(TemplateView):
    template_name = 'analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Company metrics
        companies = Company.objects.all()
        employees = Employee.objects.all()
        projects = Project.objects.all()
        
        context['company_count'] = companies.count()
        context['active_companies'] = companies.count()  # All companies are considered active
        context['total_revenue'] = sum(c.revenue for c in companies)
        
        # Employee metrics
        context['employee_count'] = employees.count()
        context['avg_salary'] = employees.aggregate(Avg('salary'))['salary__avg'] or 0
        top_performers = employees.filter(performance_rating__in=['EXC', 'GOOD']).count()
        context['top_performers'] = round((top_performers / employees.count()) * 100 if employees.count() > 0 else 0)
        
        # Project metrics
        context['active_projects'] = projects.exclude(status='COMP').count()
        context['completed_projects'] = projects.filter(status='COMP').count()
        context['avg_completion'] = round(projects.aggregate(Avg('completion_percentage'))['completion_percentage__avg'] or 0)
        
        # Department distribution data
        department_dist = Employee.objects.values('position').annotate(
            count=Count('employee_id')
        ).order_by('-count')
        
        context['department_labels'] = json.dumps([d['position'] for d in department_dist])
        context['department_data'] = json.dumps([d['count'] for d in department_dist])
        
        # Performance distribution data
        performance_dist = Employee.objects.values('performance_rating').annotate(
            count=Count('employee_id')
        ).order_by('performance_rating')
        
        context['performance_labels'] = json.dumps([d['performance_rating'] for d in performance_dist])
        context['performance_data'] = json.dumps([d['count'] for d in performance_dist])
        
        # Project timeline data
        timeline_data = []
        timeline_labels = []
        for i in range(12):
            date = timezone.now() - timezone.timedelta(days=30*i)
            count = Project.objects.filter(
                start_date__lte=date,
                status__in=['PROG', 'TEST', 'HOLD']  # Only count active projects
            ).count()
            timeline_data.append(count)
            timeline_labels.append(date.strftime('%b %Y'))
        
        context['timeline_data'] = json.dumps(list(reversed(timeline_data)))
        context['timeline_labels'] = json.dumps(list(reversed(timeline_labels)))
        
        # Top performers
        context['top_employees'] = Employee.objects.filter(
            performance_rating__in=['EXC', 'GOOD']
        ).order_by('-projects_completed')[:10]
        
        return context
