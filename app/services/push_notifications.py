from pywebpush import webpush, WebPushException
from app.core.config import settings
import json

class PushNotificationService:
    def __init__(self):
        self.vapid_private_key = settings.VAPID_PRIVATE_KEY
        self.vapid_public_key = settings.VAPID_PUBLIC_KEY
        self.vapid_claims = {"sub": settings.VAPID_CLAIM_EMAIL}
    
    def send_notification(self, subscription_info: dict, data: dict):
        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(data),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims
            )
            return True
        except WebPushException as e:
            print(f"WebPush error: {e}")
            return False

push_service = PushNotificationService()
