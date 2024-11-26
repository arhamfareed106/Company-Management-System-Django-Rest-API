from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Frontend views
    path('', views.HomeView.as_view(), name='home'),
    path('companies/', views.CompanyListView.as_view(), name='company_list'),
    path('companies/create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('companies/<slug:slug>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('companies/<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),
    path('companies/<int:pk>/employees/', views.CompanyEmployeesView.as_view(), name='company_employees'),
    
    # Employee Frontend URLs
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Analytics URL
    path('analytics/', views.AnalyticsDashboardView.as_view(), name='analytics'),
]