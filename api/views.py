from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Company, Employee, Project
from .serializers import CompanySerializer, EmployeeSerializer
from .forms import CompanyForm, EmployeeForm

# Frontend Views
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_companies'] = Company.objects.count()
        context['total_employees'] = Employee.objects.count()
        context['recent_companies'] = Company.objects.order_by('-created_at')[:5]
        context['recent_employees'] = Employee.objects.order_by('-created_at')[:5]
        return context

class CompanyListView(ListView):
    template_name = 'company_list.html'
    model = Company
    context_object_name = 'companies'

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

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company_form.html'
    success_url = reverse_lazy('company_list')

class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company_form.html'
    success_url = reverse_lazy('company_list')

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'company_confirm_delete.html'
    success_url = reverse_lazy('company_list')

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = self.object.employee_set.all()
        return context

class EmployeeListView(ListView):
    template_name = 'employee_list.html'
    model = Employee
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = Employee.objects.select_related('company').all()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(position__icontains=search) |
                Q(company__name__icontains=search)
            )
        return queryset

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

class CompanyEmployeesView(ListView):
    template_name = 'company_employees.html'
    model = Employee
    context_object_name = 'employees'

    def get_queryset(self):
        company_id = self.kwargs.get('pk')
        return Employee.objects.filter(company_id=company_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_id = self.kwargs.get('pk')
        context['company'] = Company.objects.get(id=company_id)
        return context

class AnalyticsDashboardView(TemplateView):
    template_name = 'analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic statistics
        context['total_companies'] = Company.objects.count()
        context['total_employees'] = Employee.objects.count()
        context['avg_employees_per_company'] = Employee.objects.count() / Company.objects.count() if Company.objects.count() > 0 else 0
        
        # Company statistics
        company_types = Company.objects.values('type').annotate(count=Count('id'))
        context['company_types'] = [ct['type'] for ct in company_types]
        context['company_type_counts'] = [ct['count'] for ct in company_types]
        
        # Employee distribution
        companies = Company.objects.annotate(employee_count=Count('employee'))
        context['companies'] = [comp.name for comp in companies]
        context['employee_counts'] = [comp.employee_count for comp in companies]
        
        # Additional statistics
        context['company_count'] = Company.objects.all().count()
        context['active_companies'] = Company.objects.all().count()
        context['total_revenue'] = sum(c.revenue for c in Company.objects.all())
        context['employee_count'] = Employee.objects.all().count()
        context['avg_salary'] = Employee.objects.aggregate(Avg('salary'))['salary__avg'] or 0
        top_performers = Employee.objects.filter(performance_rating__in=['EXC', 'GOOD']).count()
        context['top_performers'] = round((top_performers / Employee.objects.count()) * 100 if Employee.objects.count() > 0 else 0)
        context['active_projects'] = Project.objects.exclude(status='COMP').count()
        context['completed_projects'] = Project.objects.filter(status='COMP').count()
        context['avg_completion'] = round(Project.objects.aggregate(Avg('completion_percentage'))['completion_percentage__avg'] or 0)
        department_dist = Employee.objects.values('position').annotate(count=Count('id')).order_by('-count')
        context['department_labels'] = [d['position'] for d in department_dist]
        context['department_data'] = [d['count'] for d in department_dist]
        performance_dist = Employee.objects.values('performance_rating').annotate(count=Count('id')).order_by('performance_rating')
        context['performance_labels'] = [d['performance_rating'] for d in performance_dist]
        context['performance_data'] = [d['count'] for d in performance_dist]
        timeline_data = []
        timeline_labels = []
        for i in range(12):
            date = timezone.now() - timezone.timedelta(days=30 * i)
            count = Project.objects.filter(start_date__lte=date, status__in=['PROG', 'TEST', 'HOLD']).count()
            timeline_data.append(count)
            timeline_labels.append(date.strftime('%b %Y'))
        context['timeline_data'] = list(reversed(timeline_data))
        context['timeline_labels'] = list(reversed(timeline_labels))
        context['top_employees'] = Employee.objects.filter(performance_rating__in=['EXC', 'GOOD']).order_by('-projects_completed')[:10]
        
        return context

# API Views
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.all()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(type__icontains=search)
            )
        return queryset

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.select_related('company').all()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(position__icontains=search) |
                Q(company__name__icontains=search)
            )
        return queryset
