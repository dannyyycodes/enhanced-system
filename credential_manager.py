"""
Credential Manager
==================
Securely stores and manages API keys with encryption
"""

import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from typing import Dict, Optional
import sqlite3


class CredentialManager:
    """Manages encrypted API credentials"""
    
    def __init__(self, db_path="automation.db", master_key=None):
        self.db_path = db_path
        
        # Generate or load encryption key
        if master_key:
            self.key = self._derive_key(master_key)
        else:
            # Use environment variable or generate
            self.key = self._get_or_create_key()
        
        self.cipher = Fernet(self.key)
        self._init_credentials_table()
    
    def _get_or_create_key(self):
        """Get existing key or create new one"""
        key_file = ".encryption_key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'video_automation_salt',  # In production, use random salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _init_credentials_table(self):
        """Initialize credentials table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                encrypted_key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_credential(self, service: str, api_key: str):
        """Store an encrypted API key"""
        encrypted = self.cipher.encrypt(api_key.encode())
        encrypted_str = base64.b64encode(encrypted).decode()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO credentials (service, encrypted_key, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (service, encrypted_str))
        
        conn.commit()
        conn.close()
    
    def get_credential(self, service: str) -> Optional[str]:
        """Retrieve and decrypt an API key"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT encrypted_key FROM credentials WHERE service = ?', (service,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        encrypted = base64.b64decode(row[0])
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()
    
    def delete_credential(self, service: str):
        """Delete a credential"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM credentials WHERE service = ?', (service,))
        conn.commit()
        conn.close()
    
    def list_services(self) -> list:
        """List all services with stored credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT service, created_at FROM credentials')
        services = cursor.fetchall()
        conn.close()
        return services
    
    def get_all_credentials(self) -> Dict[str, str]:
        """Get all credentials as a dictionary"""
        services = self.list_services()
        return {service: self.get_credential(service) for service, _ in services}


# Quick setup function for initial credentials
def setup_initial_credentials():
    """Setup initial credentials from provided API keys"""
    cm = CredentialManager()
    
    credentials = {
        'kie': 'b6950bc9ee85f941ecb523ce34efb4a0',
        'blotato': 'blt_sHvjFzyhDdrJOVlCTFhV+AlHMZyeRXjE6reQL52Qxmw=',
        'openrouter': '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',
    }
    
    for service, key in credentials.items():
        cm.store_credential(service, key)
        print(f"✅ Stored {service} credential")
    
    return cm


if __name__ == '__main__':
    # Test the credential manager
    print("🔐 Setting up credential manager...")
    cm = setup_initial_credentials()
    
    print("\n📋 Stored credentials:")
    for service, created in cm.list_services():
        print(f"  • {service} (added: {created})")
    
    print("\n✅ Credential manager ready!")
