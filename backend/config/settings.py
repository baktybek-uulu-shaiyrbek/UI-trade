import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # Database
        self.database_url = os.getenv('DATABASE_URL')
        
        # Binance
        self.binance_api_key = os.getenv('BINANCE_API_KEY')
        self.binance_api_secret = os.getenv('BINANCE_API_SECRET')
        
        # JWT
        self.jwt_secret_key = os.getenv('JWT_SECRET_KEY')
        
        # Optional encryption
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        
        # Validate required settings
        required = [
            self.database_url,
            self.binance_api_key,
            self.binance_api_secret,
            self.jwt_secret_key
        ]
        
        if not all(required):
            raise ValueError("Missing required environment variables")