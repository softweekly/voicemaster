"""
System Readiness Checker for VoiceMaster Pro
Run this before setup to check if your system is ready
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_pip():
    """Check if pip is available"""
    print("📦 Checking pip (package manager)...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ pip available")
            return True
        else:
            print(f"   ❌ pip not working")
            return False
    except Exception:
        print(f"   ❌ pip not found")
        return False

def check_internet():
    """Check internet connectivity"""
    print("🌐 Checking internet connection...")
    
    try:
        import urllib.request
        urllib.request.urlopen('https://pypi.org', timeout=5)
        print("   ✅ Internet connection working")
        return True
    except Exception:
        print("   ❌ No internet connection")
        return False

def check_admin_rights():
    """Check if running with admin rights (Windows)"""
    print("🔐 Checking permissions...")
    
    try:
        # Try to write to a system location (Windows-specific test)
        if os.name == 'nt':  # Windows
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if is_admin:
                print("   ✅ Running as Administrator")
                return True
            else:
                print("   ⚠️  Not running as Administrator (recommended for setup)")
                return False
        else:
            print("   ✅ Non-Windows system")
            return True
    except Exception:
        print("   ⚠️  Could not check admin rights")
        return False

def check_disk_space():
    """Check available disk space"""
    print("💾 Checking disk space...")
    
    try:
        free_bytes = os.statvfs('.').f_frsize * os.statvfs('.').f_bavail if hasattr(os, 'statvfs') else None
        if free_bytes is None:
            # Windows fallback
            import shutil
            free_bytes = shutil.disk_usage('.').free
        
        free_mb = free_bytes / (1024 * 1024)
        
        if free_mb > 500:  # 500MB minimum
            print(f"   ✅ {free_mb:.0f}MB available")
            return True
        else:
            print(f"   ❌ Only {free_mb:.0f}MB available (need 500MB+)")
            return False
            
    except Exception:
        print("   ⚠️  Could not check disk space")
        return False

def main():
    print("🔧 VoiceMaster Pro - System Readiness Check")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Package Manager", check_pip),
        ("Internet Connection", check_internet),
        ("Permissions", check_admin_rights),
        ("Disk Space", check_disk_space)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error during {name} check: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    critical_passed = sum(1 for i, (_, result) in enumerate(results) 
                         if result and i < 3)  # First 3 are critical
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
    
    print(f"\nResults: {passed}/{len(results)} checks passed")
    
    if critical_passed >= 3:
        print("\n🎉 Your system is ready for VoiceMaster Pro!")
        print("📝 Next step: Run 'setup_for_friends.bat' as Administrator")
    else:
        print("\n⚠️  Please fix the failed checks before running setup.")
        print("\n🔧 Common fixes:")
        print("   • Install Python 3.8+ from python.org")
        print("   • Make sure 'Add Python to PATH' was checked")
        print("   • Check your internet connection")
        print("   • Free up some disk space (500MB+)")
    
    print(f"\nPress Enter to continue...")
    input()
    
    return critical_passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)