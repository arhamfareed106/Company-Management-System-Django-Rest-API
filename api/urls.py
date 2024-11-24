from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, EmployeeViewSet

# Create a DefaultRouter and register the viewsets
router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'employees', EmployeeViewSet)

# API URL configuration
urlpatterns = [
    path('', include(router.urls)),
]
