import jwt
from datetime import datetime, timedelta
import json
import logging
from config.settings import Settings

class JWTAuthenticator:
    def __init__(self):
        settings = Settings()
        self.secret_key = settings.jwt_secret_key
        self.algorithm = "HS256"
        
    def generate_token(self, user_id: str, permissions: list) -> str:
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    async def authenticate_websocket(self, auth_message: str) -> dict:
        try:
            # First message should contain JWT token
            data = json.loads(auth_message)
            token = data.get("token")
            
            if not token:
                return None
                
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            # Validate permissions for trading
            if "trading" not in payload.get("permissions", []):
                return None
                
            return payload
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            logging.error(f"JWT validation failed: {e}")
            return None