from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ViabilidadeEmpresaSerializer
from .models import ViabilidadeEmpresa

class ViabilidadeEmpresaViewSet(viewsets.ModelViewSet):
    queryset = ViabilidadeEmpresa.objects.all()
    serializer_class = ViabilidadeEmpresaSerializer

# Create your views here.
