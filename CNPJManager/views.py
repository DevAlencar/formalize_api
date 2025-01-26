from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ViabilidadeEmpresaSerializer
from .models import ViabilidadeEmpresa
from .utils.apiMercadoPago import get_link
from .serializers import PaymentSerializer  # Serializer para validação e registro
import os
from mercadopago import SDK
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ViabilidadeEmpresaViewSet(viewsets.ModelViewSet):
    queryset = ViabilidadeEmpresa.objects.all()
    serializer_class = ViabilidadeEmpresaSerializer

class PagamentoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        user = request.user
        
        link = get_link(user)

        return Response({"link": link})


# Configurar o SDK com o token de acesso do Mercado Pago
ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
mp = SDK(ACCESS_TOKEN)

class MercadoPagoWebhookViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            # Capturar os dados enviados pelo Mercado Pago
            data = request.data
            topic = data.get("type")  # Tipo de evento: "payment", "plan", etc.
            resource_id = data.get("data", {}).get("id")  # ID do pagamento
            #print("resource_id: ",resource_id)
            if topic == "payment":
                # Consultar os detalhes do pagamento na API do Mercado Pago
                payment_info = mp.payment().get(resource_id)
                payment_data = payment_info.get("response", {})

                # Verificar se o pagamento foi aprovado
                if payment_data.get("status") == "approved":
                    print("Pagamento aprovado!")
                    print(payment_data)
                    # Montar os dados para salvar no banco
                    payment_payload = {
                        "cliente_id": payment_data.get("metadata", {}).get("cliente_id"),  # Metadado customizado
                        "valor": payment_data.get("transaction_amount"),
                        "status": payment_data.get("status"),
                    }

                    # Validar e salvar os dados usando o serializer
                    serializer = PaymentSerializer(data=payment_payload)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "ignored"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Erro no webhook: {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
