#!/usr/bin/env python3
"""
System Setup Script
===================
Initializes the entire automation system
"""

import sys
import os

def setup_system():
    """Setup the complete system"""
    
    print("\n" + "="*60)
    print("🚀 Video Automation System - Initial Setup")
    print("="*60 + "\n")
    
    # Step 1: Setup credentials
    print("📝 Step 1: Setting up credentials...")
    try:
        from credential_manager import setup_initial_credentials
        cm = setup_initial_credentials()
        print("✅ Credentials configured\n")
    except Exception as e:
        print(f"❌ Credential setup failed: {e}\n")
        return False
    
    # Step 2: Initialize database
    print("📝 Step 2: Initializing database...")
    try:
        from database import Database
        db = Database()
        print("✅ Database initialized\n")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}\n")
        return False
    
    # Step 3: Setup workflow manager
    print("📝 Step 3: Setting up workflow manager...")
    try:
        from workflow_manager import setup_default_workflow
        workflow_id = setup_default_workflow()
        print(f"✅ Default workflow created (ID: {workflow_id})\n")
    except Exception as e:
        print(f"❌ Workflow manager setup failed: {e}\n")
        return False
    
    # Step 4: Test API connections
    print("📝 Step 4: Testing API connections...")
    try:
        from credential_manager import CredentialManager
        cm = CredentialManager()
        
        # Test each API
        services = {
            'kie': cm.get_credential('kie'),
            'blotato': cm.get_credential('blotato'),
            'openrouter': cm.get_credential('openrouter')
        }
        
        for service, key in services.items():
            if key:
                print(f"   ✅ {service}: configured")
            else:
                print(f"   ❌ {service}: missing")
        
        print()
    except Exception as e:
        print(f"❌ API test failed: {e}\n")
        return False
    
    # Step 5: Show summary
    print("="*60)
    print("✅ Setup Complete!")
    print("="*60 + "\n")
    
    print("🎯 Next Steps:")
    print("   1. Run: python app_enhanced.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Start chatting with your AI assistant!")
    print("\n" + "="*60 + "\n")
    
    return True


def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...\n")
    
    required = [
        'flask',
        'requests',
        'schedule',
        'cryptography'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - not installed")
            missing.append(package)
    
    print()
    
    if missing:
        print("⚠️  Missing dependencies!")
        print(f"   Run: pip install {' '.join(missing)}\n")
        print("   Or: pip install -r requirements.txt\n")
        return False
    
    return True


if __name__ == '__main__':
    print("\n")
    
    # Check dependencies first
    if not check_dependencies():
        print("❌ Please install missing dependencies first.\n")
        sys.exit(1)
    
    # Run setup
    if setup_system():
        print("🎉 System is ready to use!")
        print("\n   Run: python app_enhanced.py\n")
        sys.exit(0)
    else:
        print("❌ Setup failed. Please check errors above.\n")
        sys.exit(1)
