from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViabilidadeEmpresaViewSet, PagamentoViewSet, MercadoPagoWebhookViewSet

router = DefaultRouter()
router.register(r'viabilidades', ViabilidadeEmpresaViewSet)
router.register(r'mercadopago/pagamento', PagamentoViewSet, basename='pagamento')
router.register(r'mercadopago/webhook', MercadoPagoWebhookViewSet, basename = 'webhook')
urlpatterns = [
    path('', include(router.urls)),

]