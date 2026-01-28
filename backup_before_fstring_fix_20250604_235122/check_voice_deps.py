#!/usr/bin/env python3
"""
Check Voice Command Dependencies
"""

print("Checking voice command dependencies...")

# Test speech_recognition
try:
    import speech_recognition as sr
    print("✅ speech_recognition: OK")
except ImportError as e:
    print(f"❌ speech_recognition: MISSING - {e}")

# Test pyaudio
try:
    import pyaudio
    print("✅ pyaudio: OK")
except ImportError as e:
    print(f"❌ pyaudio: MISSING - {e}")

# Test pyttsx3
try:
    import pyttsx3
    print("✅ pyttsx3: OK")
except ImportError as e:
    print(f"❌ pyttsx3: MISSING - {e}")

# Test basic functionality
print("\nTesting basic functionality...")

try:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    print("✅ Speech recognizer created")
except Exception as e:
    print(f"❌ Speech recognizer failed: {e}")

try:
    import pyttsx3
    engine = pyttsx3.init()
    print("✅ TTS engine created")
    engine.stop()
except Exception as e:
    print(f"❌ TTS engine failed: {e}")

print("\nDone!")
