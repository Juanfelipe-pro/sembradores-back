from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings

class GoogleOAuthService:
    def verify_token(self, token: str):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            return {
                'google_id': idinfo['sub'],
                'email': idinfo['email'],
                'name': idinfo.get('name'),
                'picture': idinfo.get('picture')
            }
        except ValueError as e:
            print(f"Token verification error: {e}")
            return None

google_oauth = GoogleOAuthService()
