import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class SecureConfigManager:
    def __init__(self):
        load_dotenv()
        
        # Never commit these to version control
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        
        # Validate credentials exist
        if not all([self.api_key, self.api_secret]):
            raise ValueError("Missing required API credentials")
            
        # Optional: Additional encryption layer
        encryption_key = os.getenv('ENCRYPTION_KEY')
        if encryption_key:
            self.fernet = Fernet(encryption_key.encode())
            self.api_secret = self.decrypt_secret(self.api_secret)
    
    def decrypt_secret(self, encrypted_secret: str) -> str:
        return self.fernet.decrypt(encrypted_secret.encode()).decode()