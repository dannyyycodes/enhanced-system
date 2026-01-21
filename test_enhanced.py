#!/usr/bin/env python3
"""
System Test Script
==================
Tests all components of the enhanced system
"""

import sys

def test_imports():
    """Test that all modules can be imported"""
    print("📦 Testing imports...")
    
    modules = [
        'credential_manager',
        'workflow_manager',
        'workflow_executor',
        'ai_client',
        'database',
        'api_clients',
        'ideas'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except Exception as e:
            print(f"   ❌ {module}: {e}")
            return False
    
    print()
    return True


def test_credentials():
    """Test credential manager"""
    print("🔐 Testing credentials...")
    
    try:
        from credential_manager import CredentialManager
        cm = CredentialManager()
        
        # Check stored credentials
        services = cm.list_services()
        print(f"   Found {len(services)} stored credentials")
        
        for service, _ in services:
            key = cm.get_credential(service)
            if key:
                print(f"   ✅ {service}: {key[:10]}...")
            else:
                print(f"   ❌ {service}: not found")
        
        print()
        return len(services) >= 3  # Should have at least 3 keys
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False


def test_workflows():
    """Test workflow manager"""
    print("⚡ Testing workflow manager...")
    
    try:
        from workflow_manager import WorkflowManager
        wm = WorkflowManager()
        
        workflows = wm.list_workflows()
        print(f"   Found {len(workflows)} workflows")
        
        if workflows:
            for wf in workflows[:3]:  # Show first 3
                print(f"   • {wf['name']}: {wf['status']}")
        else:
            print("   No workflows yet (will be created on first run)")
        
        stats = wm.get_stats()
        print(f"   Stats: {stats['total_workflows']} total, {stats['active_workflows']} active")
        
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False


def test_ai_client():
    """Test AI client"""
    print("🤖 Testing AI client...")
    
    try:
        from credential_manager import CredentialManager
        from ai_client import EnhancedAIClient
        
        cm = CredentialManager()
        key = cm.get_credential('openrouter')
        
        if not key:
            print("   ⚠️  OpenRouter key not found")
            print("   (AI chat will not work until key is added)")
            print()
            return False
        
        client = EnhancedAIClient(key)
        print("   ✅ AI client initialized")
        
        # Test simple chat
        print("   Testing chat...")
        response = client.chat("Say 'OK' if you can hear me")
        
        if response and len(response) > 0:
            print(f"   ✅ AI responded: {response[:50]}...")
        else:
            print("   ❌ AI did not respond")
            return False
        
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False


def test_database():
    """Test database"""
    print("💾 Testing database...")
    
    try:
        from database import Database
        db = Database()
        
        stats = db.get_stats()
        print(f"   Total videos: {stats.get('total_videos', 0)}")
        print(f"   Total runs: {stats.get('total_runs', 0)}")
        print(f"   Success rate: {stats.get('successful_runs', 0)}/{stats.get('total_runs', 0)}")
        
        print("   ✅ Database working")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 Enhanced System Test Suite")
    print("="*60 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Credential Manager", test_credentials),
        ("Workflow Manager", test_workflows),
        ("AI Client", test_ai_client),
        ("Database", test_database),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}\n")
            results.append((name, False))
    
    # Summary
    print("="*60)
    print("📊 Test Results")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\n   Run: python app_enhanced.py")
        print("   Then open: http://localhost:5000\n")
        return 0
    else:
        print("\n⚠️  Some tests failed.")
        
        if not any(r for n, r in results if n == "Credential Manager"):
            print("\n💡 Tip: Run 'python setup.py' to configure credentials")
        
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
