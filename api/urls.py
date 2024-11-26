from django.urls import path
from .views import (
    CompanyViewSet, 
    EmployeeViewSet, 
    HomeView, 
    AnalyticsDashboardView,
    CompanyListView,
    EmployeeListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView
)

urlpatterns = [
    # Frontend URLs
    path('', HomeView.as_view(), name='home'),
    
    # Company Frontend URLs
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/update/', CompanyUpdateView.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    
    # Employee Frontend URLs
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Analytics URL
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics'),
    
    # API URLs for Companies
    path('api/companies/', CompanyViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_company_list'),
    path('api/companies/<int:pk>/', CompanyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api_company_detail'),
    
    # API URLs for Employees
    path('api/employees/', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_employee_list'),
    path('api/employees/<int:pk>/', EmployeeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api_employee_detail'),
]