import mercadopago
import os
def get_link():
    sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN"))

    # Create a preference item
    preference_data = {
        "items": [
            {
                "id": "1",
                "title": "Abertura de CNPJ",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 100
            }
        ],
        "back_urls": {
            "success": "localhost:5000/pagamentoaprovado/",
            "failure": "localhost:5000/pagamentofalhou/",
            "pending": "localhost:5000/pagamentopendente/"
        },
        "auto_return": "all",
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return preference.get("init_point")