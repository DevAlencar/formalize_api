import mercadopago
import os
from datetime import timedelta
from django.utils import timezone

def get_link(user):
    sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN"))

    # Generate unique reference
    external_reference = f"CNPJ_{user.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}"

    preference_data = {
        "items": [
            {
                "id": "1", 
                "title": "Abertura de CNPJ",
                "description": "Serviço de abertura e registro de CNPJ",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 100,
                "category_id": "services"
            }
        ],
        "back_urls": {
            "success": "localhost:5000/pagamentoaprovado/",
            "failure": "localhost:5000/pagamentofalhou/",
            "pending": "localhost:5000/pagamentopendente/"
        },
        "metadata": {
            "cliente_id": user.id,
            "cliente_email": user.email,
            "cliente_nome": user.get_full_name()
        },
        "payer": {
            "name": user.get_full_name(),
            "email": user.email
        },
        "external_reference": external_reference,  # Identificador único
        "expires": True,
        "expiration_date_from": timezone.now().isoformat(),
        "expiration_date_to": (timezone.now() + timedelta(hours=24)).isoformat(),
        "statement_descriptor": "FORMALIZE.CA",
        "auto_return": "approved",
        "binary_mode": True,  # Aceita apenas aprovado ou rejeitado
        "notification_url": "https://clever-magical-yak.ngrok-free.app/api/v1/cnpjmanager/mercadopago/webhook/"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return preference.get("init_point")