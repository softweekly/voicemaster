import sys
print(f"Python version: {sys.version}")

try:
    import aifc
    print("✅ aifc module available")
except ImportError as e:
    print(f"❌ aifc module error: {e}")

try:
    import audioop  
    print("✅ audioop module available")
except ImportError as e:
    print(f"❌ audioop module error: {e}")

try:
    import distutils
    print("✅ distutils module available")
except ImportError as e:
    print(f"❌ distutils module error: {e}")

try:
    import speech_recognition as sr
    print("✅ speech_recognition module available")
except ImportError as e:
    print(f"❌ speech_recognition module error: {e}")

print("\nTesting speech recognition functionality...")
try:
    from app_logic import speech_to_text, record_audio
    print("✅ Speech-to-Clone functions can be imported")
except Exception as e:
    print(f"❌ Speech-to-Clone import error: {e}")

input("Press Enter to continue...")