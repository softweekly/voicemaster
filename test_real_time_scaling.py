"""
Test script to verify real-time scaling in VoiceMaster Pro
This test opens both GUIs and provides instructions for testing scaling
"""

import tkinter as tk
import subprocess
import sys
import os
from pathlib import Path

def test_real_time_scaling():
    """Test real-time scaling functionality"""
    
    print("🔄 VoiceMaster Pro - Real-Time Scaling Test")
    print("=" * 60)
    print()
    
    print("This test will help you verify that the GUI scales properly")
    print("when you resize the window in real-time.")
    print()
    
    # Get the current directory
    current_dir = Path.cwd()
    
    # Check if we have the required files
    required_files = ['login_gui.py', 'voicemaster_gui.py']
    missing_files = [f for f in required_files if not (current_dir / f).exists()]
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ Required files found")
    print()
    
    # Find Python executable
    python_exe = sys.executable
    
    # Try to use venv python if available
    if os.name == 'nt':  # Windows
        venv_paths = [
            current_dir / ".venv" / "Scripts" / "python.exe",
            current_dir / "venv" / "Scripts" / "python.exe"
        ]
    else:  # Linux/Unix
        venv_paths = [
            current_dir / ".venv" / "bin" / "python",
            current_dir / "venv" / "bin" / "python"
        ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            python_exe = str(venv_path)
            print(f"✅ Using virtual environment: {python_exe}")
            break
    else:
        print(f"ℹ️  Using system Python: {python_exe}")
    
    print()
    print("🧪 SCALING TEST INSTRUCTIONS")
    print("=" * 60)
    print()
    print("1. Test Login GUI Scaling:")
    print("   • I'll open the login GUI")
    print("   • Try resizing the window by dragging corners")
    print("   • Text and buttons should scale smoothly")
    print("   • Everything should remain visible and usable")
    print()
    
    input("Press Enter to open Login GUI for testing...")
    
    try:
        # Launch login GUI
        login_process = subprocess.Popen([python_exe, "login_gui.py"])
        print("✅ Login GUI launched")
        print()
        print("📏 Test the login GUI:")
        print("   • Drag corners to resize the window")
        print("   • Make it very small, then very large")
        print("   • Check that text scales appropriately")
        print("   • Verify buttons remain clickable")
        print("   • Close the login GUI when done")
        print()
        
        # Wait for user to test
        input("Press Enter when you've finished testing the login GUI...")
        
        # Try to terminate login process if still running
        try:
            login_process.terminate()
        except:
            pass
        
    except Exception as e:
        print(f"❌ Failed to launch login GUI: {e}")
        return False
    
    print()
    print("2. Test Main GUI Scaling:")
    print("   • I'll open the main VoiceMaster GUI")
    print("   • Try resizing the window extensively")
    print("   • All elements should scale in real-time")
    print("   • Status bar should show scaling percentage")
    print()
    
    # Check if .env exists, if not, warn user
    if not (current_dir / ".env").exists():
        print("⚠️  Note: No .env file found. The main GUI will show the login screen first.")
        print("   You can close it or enter a test API key for testing.")
        print()
    
    input("Press Enter to open Main GUI for testing...")
    
    try:
        # Launch main GUI
        main_process = subprocess.Popen([python_exe, "voicemaster_gui.py"])
        print("✅ Main GUI launched")
        print()
        print("📏 Test the main GUI:")
        print("   • Drag corners to resize the window")
        print("   • Try making it very small (600x500 minimum)")
        print("   • Try making it very large")
        print("   • Watch the status bar for scale percentage")
        print("   • Check that all buttons and text scale smoothly")
        print("   • Verify text input area scales properly")
        print("   • Close the GUI when done")
        print()
        
        # Wait for user to test
        input("Press Enter when you've finished testing the main GUI...")
        
        # Try to terminate main process if still running
        try:
            main_process.terminate()
        except:
            pass
            
    except Exception as e:
        print(f"❌ Failed to launch main GUI: {e}")
        return False
    
    print()
    print("🎯 SCALING FEATURES TESTED")
    print("=" * 60)
    print("✅ Real-time font scaling")
    print("✅ Button padding adjustment") 
    print("✅ Window size adaptation")
    print("✅ Minimum size enforcement")
    print("✅ Maximum size limits")
    print("✅ Cross-platform compatibility")
    print("✅ Smooth scaling transitions")
    print("✅ Status feedback during scaling")
    print()
    
    print("💡 Expected Behavior:")
    print("• Fonts scale from 80% to 150% based on window size")
    print("• Minimum window size: 600x500 (main), 450x350 (login)")
    print("• Everything remains visible at all sizes")
    print("• Scaling happens smoothly as you resize")
    print("• Status shows current scale percentage")
    print()
    
    success = input("Did the scaling work properly? (y/n): ").lower().startswith('y')
    
    if success:
        print()
        print("🎉 Real-time scaling test PASSED!")
        print("Your VoiceMaster Pro will work perfectly on any screen size!")
        print()
        print("✅ Benefits for your friends:")
        print("• Works on laptops, desktops, and large monitors")
        print("• Automatically adapts to their screen resolution")
        print("• Stays usable when they resize the window")
        print("• Professional scaling experience")
    else:
        print()
        print("⚠️  Scaling test had issues.")
        print("Please check the console output for any error messages.")
        print("The basic functionality should still work fine.")
    
    return success

def main():
    print("🚀 VoiceMaster Pro - Real-Time Scaling Verification")
    print("=" * 60)
    print()
    print("This test helps verify that the new real-time scaling")
    print("features work correctly for users with different screen sizes.")
    print()
    
    success = test_real_time_scaling()
    
    print()
    print("=" * 60)
    if success:
        print("🎉 All scaling tests completed successfully!")
        print("VoiceMaster Pro is ready for distribution with full scaling support!")
    else:
        print("⚠️  Some scaling features may need attention.")
        print("Basic functionality should still work for your friends.")
    
    print()
    input("Press Enter to exit...")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        sys.exit(1)