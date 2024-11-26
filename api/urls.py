from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, EmployeeViewSet, HomeView, AnalyticsDashboardView

# Create a router for API endpoints
router = DefaultRouter()
router.register(r'api/companies', CompanyViewSet, basename='company-api')
router.register(r'api/employees', EmployeeViewSet, basename='employee-api')

# URL patterns for both API and frontend views
urlpatterns = [
    # Home page
    path('', HomeView.as_view(), name='home'),
    
    # Analytics Dashboard
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    
    # API URLs
    path('', include(router.urls)),
    
    # Frontend URLs
    path('companies/', CompanyViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='company-list'),
    
    path('companies/<int:pk>/', CompanyViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='company-detail'),
    
    path('companies/create/', CompanyViewSet.as_view({
        'get': 'create',
        'post': 'create'
    }), name='company-create'),
    
    path('companies/<int:pk>/employees/', CompanyViewSet.as_view({
        'get': 'employees'
    }), name='company-employees'),
    
    path('employees/', EmployeeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='employee-list'),
    
    path('employees/<int:pk>/', EmployeeViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='employee-detail'),
    
    path('employees/create/', EmployeeViewSet.as_view({
        'get': 'create',
        'post': 'create'
    }), name='employee-create'),
    
    path('employees/<int:pk>/edit/', EmployeeViewSet.as_view({
        'get': 'update',
        'put': 'update'
    }), name='employee-edit'),
]
