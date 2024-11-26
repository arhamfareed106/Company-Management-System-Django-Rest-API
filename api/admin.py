from django.contrib import admin
from .models import Company, Employee, Project

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'website', 'established_date', 'get_employee_count')
    search_fields = ('name', 'location', 'type')
    list_filter = ('type', 'established_date')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    ordering = ('name',)

    def get_employee_count(self, obj):
        return obj.employee_set.count()
    get_employee_count.short_description = 'Employees'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'position', 'company', 'hire_date', 'is_active')
    search_fields = ('name', 'email', 'phone', 'company__name')
    list_filter = ('position', 'company', 'is_active', 'hire_date')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'status', 'start_date', 'end_date', 'get_employee_count')
    search_fields = ('name', 'company__name', 'description')
    list_filter = ('status', 'company', 'start_date')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('employees',)
    ordering = ('-start_date',)

    def get_employee_count(self, obj):
        return obj.employees.count()
    get_employee_count.short_description = 'Team Size'
