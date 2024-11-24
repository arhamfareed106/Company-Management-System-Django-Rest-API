from django.contrib import admin
from django.urls import include, path
from api.views import CompanyViewSet, EmployeeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', include(router.urls)),  # API routes
]
