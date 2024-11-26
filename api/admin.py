from django.contrib import admin
from .models import Company, Employee

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'about', 'type', 'added_date', 'active')
    search_fields = ('name', 'location')
    list_filter = ('type', 'active')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'phone', 'about', 'position', 'company')
    search_fields = ('name', 'email')
    list_filter = ('position', 'company')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
