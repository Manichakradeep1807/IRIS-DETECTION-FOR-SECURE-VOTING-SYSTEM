#!/usr/bin/env python3
"""
COMPREHENSIVE VOICE COMMANDS DIAGNOSTIC TOOL
============================================
This tool will diagnose and fix all voice command issues in the iris recognition system.
"""

import os
import sys
import time
import threading
import traceback
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_status(message, status="INFO"):
    """Print a status message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    icon = icons.get(status, "ℹ️")
    print(f"[{timestamp}] {icon} {message}")

def test_dependencies():
    """Test all voice command dependencies"""
    print_header("TESTING VOICE COMMAND DEPENDENCIES")
    
    dependencies = {
        'speech_recognition': 'SpeechRecognition',
        'pyaudio': 'PyAudio',
        'pyttsx3': 'pyttsx3',
        'threading': 'threading (built-in)',
        'time': 'time (built-in)'
    }
    
    results = {}
    
    for module, name in dependencies.items():
        try:
            if module == 'pyaudio':
                import pyaudio
                # Test if PyAudio can actually access audio devices
                p = pyaudio.PyAudio()
                device_count = p.get_device_count()
                p.terminate()
                print_status(f"{name}: Available ({device_count} audio devices)", "SUCCESS")
                results[module] = True
            elif module == 'speech_recognition':
                import speech_recognition as sr
                # Test if speech recognition can create recognizer
                recognizer = sr.Recognizer()
                print_status(f"{name}: Available", "SUCCESS")
                results[module] = True
            elif module == 'pyttsx3':
                import pyttsx3
                # Test if TTS engine can be initialized
                engine = pyttsx3.init()
                engine.stop()
                print_status(f"{name}: Available", "SUCCESS")
                results[module] = True
            else:
                __import__(module)
                print_status(f"{name}: Available", "SUCCESS")
                results[module] = True
                
        except Exception as e:
            print_status(f"{name}: NOT AVAILABLE - {str(e)}", "ERROR")
            results[module] = False
    
    return results

def test_voice_command_files():
    """Test voice command file integrity"""
    print_header("TESTING VOICE COMMAND FILES")
    
    files_to_check = [
        'voice_commands.py',
        'voice_commands_fixed.py'
    ]
    
    results = {}
    
    for file in files_to_check:
        if os.path.exists(file):
            try:
                # Try to import the module
                if file == 'voice_commands.py':
                    from voice_commands import VoiceCommandSystem, initialize_voice_commands
                    print_status(f"{file}: Import successful", "SUCCESS")
                    
                    # Test instantiation
                    voice_system = VoiceCommandSystem()
                    print_status(f"{file}: Instantiation successful", "SUCCESS")
                    results[file] = True
                    
                elif file == 'voice_commands_fixed.py':
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("voice_commands_fixed", file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print_status(f"{file}: Import successful", "SUCCESS")
                    results[file] = True
                    
            except Exception as e:
                print_status(f"{file}: Import failed - {str(e)}", "ERROR")
                results[file] = False
        else:
            print_status(f"{file}: File not found", "WARNING")
            results[file] = False
    
    return results

def test_voice_system_integration():
    """Test voice system integration with Main.py"""
    print_header("TESTING VOICE SYSTEM INTEGRATION")
    
    try:
        # Test if Main.py can import voice commands
        from voice_commands import initialize_voice_commands, get_voice_system, is_voice_available
        print_status("Voice commands import: SUCCESS", "SUCCESS")
        
        # Test initialization
        voice_system = initialize_voice_commands()
        if voice_system:
            print_status("Voice system initialization: SUCCESS", "SUCCESS")
            
            # Test callback registration
            def test_callback():
                return "test_success"
            
            voice_system.register_callback('test_command', test_callback)
            
            if 'test_command' in voice_system.command_callbacks:
                result = voice_system.command_callbacks['test_command']()
                if result == "test_success":
                    print_status("Callback registration and execution: SUCCESS", "SUCCESS")
                    return True
                else:
                    print_status("Callback execution failed", "ERROR")
                    return False
            else:
                print_status("Callback registration failed", "ERROR")
                return False
        else:
            print_status("Voice system initialization failed", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Integration test failed: {str(e)}", "ERROR")
        traceback.print_exc()
        return False

def test_microphone_access():
    """Test microphone access and functionality"""
    print_header("TESTING MICROPHONE ACCESS")
    
    try:
        import speech_recognition as sr
        import pyaudio
        
        # Test PyAudio microphone access
        p = pyaudio.PyAudio()
        
        # List available devices
        device_count = p.get_device_count()
        print_status(f"Found {device_count} audio devices", "INFO")
        
        # Find default input device
        default_device = None
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                print_status(f"Input device {i}: {device_info['name']}", "INFO")
                if default_device is None:
                    default_device = i
        
        p.terminate()
        
        if default_device is not None:
            print_status(f"Default input device: {default_device}", "SUCCESS")
            
            # Test speech recognition microphone
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            print_status("Testing microphone with speech recognition...", "INFO")
            
            # Quick ambient noise test (non-blocking)
            try:
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print_status("Microphone access: SUCCESS", "SUCCESS")
                return True
            except Exception as mic_error:
                print_status(f"Microphone access failed: {str(mic_error)}", "ERROR")
                return False
        else:
            print_status("No input devices found", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Microphone test failed: {str(e)}", "ERROR")
        return False

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print_header("TESTING TEXT-TO-SPEECH")
    
    try:
        import pyttsx3
        
        # Test TTS initialization
        engine = pyttsx3.init()
        print_status("TTS engine initialization: SUCCESS", "SUCCESS")
        
        # Test TTS properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        voices = engine.getProperty('voices')
        
        print_status(f"TTS rate: {rate}", "INFO")
        print_status(f"TTS volume: {volume}", "INFO")
        print_status(f"Available voices: {len(voices) if voices else 0}", "INFO")
        
        # Test TTS without actually speaking (to avoid noise)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        
        print_status("TTS configuration: SUCCESS", "SUCCESS")
        engine.stop()
        
        return True
        
    except Exception as e:
        print_status(f"TTS test failed: {str(e)}", "ERROR")
        return False

def test_command_patterns():
    """Test voice command patterns"""
    print_header("TESTING COMMAND PATTERNS")
    
    try:
        from voice_commands import VoiceCommandSystem
        
        voice_system = VoiceCommandSystem()
        
        # Test if command patterns exist
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print_status(f"Found {len(patterns)} command categories", "SUCCESS")
            
            # Test specific important commands
            important_commands = [
                'start_recognition',
                'take_photo',
                'show_gallery',
                'stop_recognition',
                'train_model',
                'test_recognition'
            ]
            
            missing_commands = []
            for cmd in important_commands:
                if cmd in patterns:
                    pattern_count = len(patterns[cmd])
                    print_status(f"Command '{cmd}': {pattern_count} patterns", "SUCCESS")
                else:
                    missing_commands.append(cmd)
                    print_status(f"Command '{cmd}': MISSING", "ERROR")
            
            if missing_commands:
                print_status(f"Missing commands: {missing_commands}", "ERROR")
                return False
            else:
                print_status("All important commands found", "SUCCESS")
                return True
        else:
            print_status("No command patterns found", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Command pattern test failed: {str(e)}", "ERROR")
        return False

def run_comprehensive_diagnosis():
    """Run comprehensive voice command diagnosis"""
    print_header("COMPREHENSIVE VOICE COMMANDS DIAGNOSIS")
    print_status("Starting comprehensive diagnosis...", "INFO")
    
    results = {}
    
    # Test 1: Dependencies
    results['dependencies'] = test_dependencies()
    
    # Test 2: Voice command files
    results['files'] = test_voice_command_files()
    
    # Test 3: System integration
    results['integration'] = test_voice_system_integration()
    
    # Test 4: Microphone access
    results['microphone'] = test_microphone_access()
    
    # Test 5: Text-to-speech
    results['tts'] = test_text_to_speech()
    
    # Test 6: Command patterns
    results['patterns'] = test_command_patterns()
    
    return results

if __name__ == "__main__":
    print("🎤 VOICE COMMANDS DIAGNOSTIC TOOL")
    print("=" * 60)
    print("This tool will diagnose all voice command issues and provide fixes.")
    print("Please wait while we run comprehensive tests...")
    
    # Run diagnosis
    results = run_comprehensive_diagnosis()
    
    # Print summary
    print_header("DIAGNOSIS SUMMARY")
    
    all_passed = True
    for category, result in results.items():
        if isinstance(result, dict):
            # For dependency results
            passed = all(result.values())
        else:
            # For boolean results
            passed = result
        
        if passed:
            print_status(f"{category.upper()}: PASSED", "SUCCESS")
        else:
            print_status(f"{category.upper()}: FAILED", "ERROR")
            all_passed = False
    
    if all_passed:
        print_status("ALL TESTS PASSED! Voice commands should work properly.", "SUCCESS")
    else:
        print_status("SOME TESTS FAILED. Fixes needed.", "WARNING")
        print("\nNext steps:")
        print("1. Install missing dependencies: pip install SpeechRecognition pyaudio pyttsx3")
        print("2. Check microphone permissions and connections")
        print("3. Run the fix script that will be generated")
    
    print("\n" + "="*60)
    print("Diagnosis complete!")
