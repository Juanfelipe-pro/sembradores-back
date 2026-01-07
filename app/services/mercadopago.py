import mercadopago
from app.core.config import settings

class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN) if settings.MP_ACCESS_TOKEN else None
    
    def crear_preferencia(self, titulo: str, precio: int, user_id: str):
        if not self.sdk:
            raise Exception("MercadoPago no configurado")
        
        preference_data = {
            "items": [
                {
                    "title": titulo,
                    "quantity": 1,
                    "unit_price": float(precio / 100),
                }
            ],
            "back_urls": {
                "success": f"{settings.FRONTEND_URL}/pago/success",
                "failure": f"{settings.FRONTEND_URL}/pago/failure",
                "pending": f"{settings.FRONTEND_URL}/pago/pending"
            },
            "auto_return": "approved",
            "external_reference": str(user_id),
        }
        
        preference = self.sdk.preference().create(preference_data)
        return preference["response"]
    
    def get_payment(self, payment_id: str):
        if not self.sdk:
            return None
        payment = self.sdk.payment().get(payment_id)
        return payment["response"]

mp_service = MercadoPagoService()
