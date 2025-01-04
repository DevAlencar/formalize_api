from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViabilidadeEmpresaViewSet

router = DefaultRouter()
router.register(r'viabilidades', ViabilidadeEmpresaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include('allauth.urls')),

]