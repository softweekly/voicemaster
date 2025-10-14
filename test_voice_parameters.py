#!/usr/bin/env python3
"""
Test script for voice parameter functionality
"""

import os
from app_logic import text_to_speech

def test_voice_parameters():
    """Test the new voice parameter functionality"""
    print("Testing voice parameter functionality...")
    print("=" * 50)
    
    # Test text
    test_text = "Testing voice parameters with different settings."
    
    # Test default parameters
    print("1. Testing default parameters...")
    result1 = text_to_speech(
        test_text, 
        filename="test_default.mp3"
    )
    if result1:
        print(f"✓ Default parameters test successful: {result1}")
    else:
        print("✗ Default parameters test failed")
    
    # Test custom parameters
    print("\n2. Testing custom parameters...")
    result2 = text_to_speech(
        test_text,
        filename="test_custom.mp3",
        stability=0.8,
        similarity_boost=0.9,
        style=0.3,
        speed=1.2
    )
    if result2:
        print(f"✓ Custom parameters test successful: {result2}")
    else:
        print("✗ Custom parameters test failed")
    
    # Test parameter validation
    print("\n3. Testing parameter ranges...")
    result3 = text_to_speech(
        test_text,
        filename="test_ranges.mp3",
        stability=0.0,      # Minimum stability
        similarity_boost=1.0,  # Maximum similarity
        style=1.0,          # Maximum style
        speed=0.5           # Slower speed
    )
    if result3:
        print(f"✓ Parameter ranges test successful: {result3}")
    else:
        print("✗ Parameter ranges test failed")
    
    print("\n" + "=" * 50)
    print("Voice parameter testing complete!")
    
    # Show generated files
    print("\nGenerated test files:")
    for file in ["test_default.mp3", "test_custom.mp3", "test_ranges.mp3"]:
        filepath = os.path.join("generated_audio", file)
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} (not found)")

if __name__ == "__main__":
    # Make sure we have an API key for testing
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("⚠️  No ELEVENLABS_API_KEY found in environment.")
        print("   Voice parameter functions are ready, but API testing requires a valid key.")
        print("   The GUI sliders and parameter passing are implemented and ready to use!")
    else:
        print(f"🔑 Found API key: {api_key[:8]}...")
        test_voice_parameters()