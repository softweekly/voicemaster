"""
Test script for VoiceMaster Pro login system
This script helps verify the login system is working correctly
"""

import os
import sys
from pathlib import Path

def test_file_structure():
    """Test that required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        "login_gui.py",
        "voicemaster_gui.py", 
        "app_logic.py",
        "launch_voicemaster.bat",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_env_file_creation():
    """Test .env file creation capability"""
    print("\n🔧 Testing .env file creation...")
    
    # Backup existing .env if it exists
    env_path = Path(".env")
    backup_path = Path(".env.backup")
    
    had_existing = env_path.exists()
    if had_existing:
        print("📋 Backing up existing .env file...")
        env_path.rename(backup_path)
    
    # Test creating .env file
    try:
        with open(".env", "w") as f:
            f.write('ELEVENLABS_API_KEY="test_key_12345"\n')
        print("✅ .env file creation successful")
        
        # Clean up test file
        env_path.unlink()
        
        # Restore backup if it existed
        if had_existing:
            backup_path.rename(env_path)
            print("📋 Restored original .env file")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        
        # Restore backup if it existed
        if had_existing and backup_path.exists():
            backup_path.rename(env_path)
        
        return False

def test_python_imports():
    """Test that required Python modules can be imported"""
    print("\n📦 Testing Python imports...")
    
    required_modules = [
        "tkinter",
        "requests", 
        "os",
        "json",
        "pathlib",
        "subprocess"
    ]
    
    failed_imports = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required modules available")
        return True

def test_login_gui_syntax():
    """Test that login_gui.py has valid syntax"""
    print("\n🐍 Testing login_gui.py syntax...")
    
    try:
        with open("login_gui.py", "r") as f:
            code = f.read()
        
        compile(code, "login_gui.py", "exec")
        print("✅ login_gui.py syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in login_gui.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading login_gui.py: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 VoiceMaster Pro - Login System Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Environment File", test_env_file_creation),
        ("Python Imports", test_python_imports),
        ("Login GUI Syntax", test_login_gui_syntax)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Login system should work correctly.")
        print("\n🚀 To test the login system:")
        print("   1. Delete .env file if it exists")
        print("   2. Double-click launch_voicemaster.bat")
        print("   3. The login GUI should appear automatically")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before using the login system.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    
    print("\nPress Enter to continue...")
    input()
    
    sys.exit(0 if success else 1)