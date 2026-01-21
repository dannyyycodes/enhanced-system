#!/usr/bin/env python3
"""
Test Script
===========
Verify that the system is configured correctly
"""

import sys
from config import Config, check_config

def test_imports():
    """Test that all dependencies are installed"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("  ✅ Flask")
    except ImportError:
        print("  ❌ Flask - run: pip install flask")
        return False
    
    try:
        import requests
        print("  ✅ Requests")
    except ImportError:
        print("  ❌ Requests - run: pip install requests")
        return False
    
    try:
        import schedule
        print("  ✅ Schedule")
    except ImportError:
        print("  ❌ Schedule - run: pip install schedule")
        return False
    
    return True


def test_config():
    """Test configuration"""
    print("\n🔍 Testing configuration...")
    
    if check_config():
        print("  ✅ All API keys configured")
        return True
    else:
        print("  ❌ Some API keys missing")
        return False


def test_database():
    """Test database creation"""
    print("\n🔍 Testing database...")
    
    try:
        from database import Database
        db = Database(":memory:")  # Use in-memory database for testing
        
        # Try to get stats
        stats = db.get_stats()
        print("  ✅ Database working")
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False


def test_ideas():
    """Test ideas module"""
    print("\n🔍 Testing ideas bank...")
    
    try:
        from ideas import get_next_idea, IDEAS
        
        if len(IDEAS) == 0:
            print("  ❌ No ideas in bank")
            return False
        
        idea, _ = get_next_idea()
        
        required_fields = ['slug', 'coreHook', 'coreAction']
        for field in required_fields:
            if field not in idea:
                print(f"  ❌ Idea missing field: {field}")
                return False
        
        print(f"  ✅ Ideas bank ({len(IDEAS)} ideas)")
        return True
    except Exception as e:
        print(f"  ❌ Ideas error: {e}")
        return False


def test_workflow():
    """Test workflow engine (without running)"""
    print("\n🔍 Testing workflow engine...")
    
    try:
        from workflow import WorkflowEngine
        
        # Just test initialization
        engine = WorkflowEngine()
        print("  ✅ Workflow engine initialized")
        return True
    except Exception as e:
        print(f"  ❌ Workflow error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("🧪 Video Automation System - Test Suite")
    print("="*50 + "\n")
    
    tests = [
        ("Dependencies", test_imports),
        ("Configuration", test_config),
        ("Database", test_database),
        ("Ideas Bank", test_ideas),
        ("Workflow Engine", test_workflow),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Results")
    print("="*50 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to go.")
        print("\nRun: python app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
