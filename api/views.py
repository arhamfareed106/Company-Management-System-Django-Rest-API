from django.shortcuts import render
from api import serializers
from rest_framework import viewsets # type: ignore
from api.models import Company
from api.serializers import CompanySerializer
# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset=Company.objects.all
    serializer_class=CompanySerializer
    
    
    
    
    