#!/usr/bin/env python3
"""
Debug script to test voice generation with different parameter combinations
"""

import os
import sys
from app_logic import text_to_speech

def test_voice_generation():
    """Test voice generation with different parameter sets"""
    print("Testing voice generation with different parameters...")
    print("=" * 60)
    
    # Check if API key is available
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ No ELEVENLABS_API_KEY found in environment!")
        print("Please check your .env file or environment variables.")
        return
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    test_text = "Hello, this is a test message."
    
    # Test 1: Minimal parameters (like original)
    print("\n1️⃣ Testing with minimal parameters...")
    result1 = text_to_speech(test_text, filename="debug_test1.mp3")
    if result1:
        print(f"✅ Success: {result1}")
    else:
        print("❌ Failed with minimal parameters")
    
    # Test 2: Basic voice settings only
    print("\n2️⃣ Testing with basic voice settings...")
    result2 = text_to_speech(
        test_text, 
        filename="debug_test2.mp3",
        stability=0.5,
        similarity_boost=0.75
    )
    if result2:
        print(f"✅ Success: {result2}")
    else:
        print("❌ Failed with basic voice settings")
    
    # Test 3: With style parameter
    print("\n3️⃣ Testing with style parameter...")
    result3 = text_to_speech(
        test_text, 
        filename="debug_test3.mp3",
        stability=0.5,
        similarity_boost=0.75,
        style=0.2
    )
    if result3:
        print(f"✅ Success: {result3}")
    else:
        print("❌ Failed with style parameter")
    
    # Test 4: Check if issue is with v2 model
    print("\n4️⃣ Testing if issue is with model version...")
    # We'll modify the function temporarily to test v1
    print("Note: This test uses the current implementation")
    result4 = text_to_speech(
        test_text, 
        filename="debug_test4.mp3",
        stability=0.6,
        similarity_boost=0.8
    )
    if result4:
        print(f"✅ Success: {result4}")
    else:
        print("❌ Failed - might be model version issue")
    
    print("\n" + "=" * 60)
    print("Debug testing complete!")
    
    # Show which files were created
    print("\nGenerated files:")
    for i in range(1, 5):
        filepath = os.path.join("generated_audio", f"debug_test{i}.mp3")
        if os.path.exists(filepath):
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath} (not created)")

if __name__ == "__main__":
    test_voice_generation()