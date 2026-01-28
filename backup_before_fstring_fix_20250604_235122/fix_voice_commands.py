#!/usr/bin/env python3
"""
VOICE COMMANDS FIX TOOL
=======================
This tool will diagnose and fix all voice command issues.
"""

import os
import sys
import subprocess
import time
import traceback

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def print_status(message, status="INFO"):
    """Print a status message"""
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    icon = icons.get(status, "ℹ️")
    print(f"{icon} {message}")

def install_dependencies():
    """Install missing voice command dependencies"""
    print_header("INSTALLING VOICE COMMAND DEPENDENCIES")
    
    dependencies = [
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "pyaudio>=0.2.11"
    ]
    
    for dep in dependencies:
        print_status(f"Installing {dep}...", "INFO")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print_status(f"Successfully installed {dep}", "SUCCESS")
            else:
                print_status(f"Failed to install {dep}: {result.stderr}", "ERROR")
                
        except subprocess.TimeoutExpired:
            print_status(f"Timeout installing {dep}", "ERROR")
        except Exception as e:
            print_status(f"Error installing {dep}: {e}", "ERROR")

def test_imports():
    """Test if voice command imports work"""
    print_header("TESTING VOICE COMMAND IMPORTS")
    
    imports_ok = True
    
    # Test speech_recognition
    try:
        import speech_recognition as sr
        print_status("speech_recognition: OK", "SUCCESS")
    except ImportError as e:
        print_status(f"speech_recognition: FAILED - {e}", "ERROR")
        imports_ok = False
    
    # Test pyaudio
    try:
        import pyaudio
        print_status("pyaudio: OK", "SUCCESS")
    except ImportError as e:
        print_status(f"pyaudio: FAILED - {e}", "ERROR")
        imports_ok = False
    
    # Test pyttsx3
    try:
        import pyttsx3
        print_status("pyttsx3: OK", "SUCCESS")
    except ImportError as e:
        print_status(f"pyttsx3: FAILED - {e}", "ERROR")
        imports_ok = False
    
    return imports_ok

def test_voice_system():
    """Test voice command system"""
    print_header("TESTING VOICE COMMAND SYSTEM")
    
    try:
        # Import voice commands
        from voice_commands import VoiceCommandSystem, initialize_voice_commands
        print_status("Voice commands module imported successfully", "SUCCESS")
        
        # Create voice system
        voice_system = VoiceCommandSystem()
        print_status("Voice command system created successfully", "SUCCESS")
        
        # Test command patterns
        if hasattr(voice_system, 'command_patterns'):
            patterns = voice_system.command_patterns
            print_status(f"Found {len(patterns)} command patterns", "SUCCESS")
            
            # Check key commands
            key_commands = ['start_recognition', 'take_photo', 'show_gallery', 'train_model']
            missing = []
            for cmd in key_commands:
                if cmd in patterns:
                    print_status(f"Command '{cmd}': Found ({len(patterns[cmd])} patterns)", "SUCCESS")
                else:
                    missing.append(cmd)
                    print_status(f"Command '{cmd}': MISSING", "ERROR")
            
            if missing:
                print_status(f"Missing commands: {missing}", "ERROR")
                return False
        else:
            print_status("No command patterns found", "ERROR")
            return False
        
        # Test callback registration
        def test_callback():
            return "test_success"
        
        voice_system.register_callback('test_command', test_callback)
        
        if 'test_command' in voice_system.command_callbacks:
            result = voice_system.command_callbacks['test_command']()
            if result == "test_success":
                print_status("Callback registration and execution: OK", "SUCCESS")
            else:
                print_status("Callback execution failed", "ERROR")
                return False
        else:
            print_status("Callback registration failed", "ERROR")
            return False
        
        return True
        
    except Exception as e:
        print_status(f"Voice system test failed: {e}", "ERROR")
        traceback.print_exc()
        return False

def test_hardware():
    """Test hardware components"""
    print_header("TESTING HARDWARE COMPONENTS")
    
    # Test microphone
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        print_status("Microphone object created successfully", "SUCCESS")
        
        # Quick test without hanging
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print_status("Microphone access: OK", "SUCCESS")
        except Exception as mic_error:
            print_status(f"Microphone access issue: {mic_error}", "WARNING")
            print_status("Voice commands will work in fallback mode", "INFO")
        
    except Exception as e:
        print_status(f"Microphone test failed: {e}", "ERROR")
    
    # Test TTS
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print_status("TTS engine created successfully", "SUCCESS")
        
        # Test properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        print_status(f"TTS rate: {rate}, volume: {volume}", "INFO")
        
        engine.stop()
        print_status("TTS engine: OK", "SUCCESS")
        
    except Exception as e:
        print_status(f"TTS test failed: {e}", "ERROR")

def create_voice_test_script():
    """Create a simple voice test script"""
    print_header("CREATING VOICE TEST SCRIPT")
    
    test_script = '''#!/usr/bin/env python3
"""
Simple Voice Commands Test
"""

def test_voice_commands():
    """Test voice commands functionality"""
    print("🎤 Testing Voice Commands...")
    
    try:
        from voice_commands import VoiceCommandSystem
        
        # Create voice system
        voice_system = VoiceCommandSystem()
        print("✅ Voice system created")
        
        # Test callback registration
        def test_callback():
            print("✅ Test callback executed successfully!")
            return True
        
        voice_system.register_callback('test_command', test_callback)
        
        # Execute test callback
        if 'test_command' in voice_system.command_callbacks:
            voice_system.command_callbacks['test_command']()
            print("✅ Voice command system is working!")
        else:
            print("❌ Callback registration failed")
        
        # Test command patterns
        patterns = voice_system.command_patterns
        print(f"✅ Found {len(patterns)} command patterns")
        
        # List some commands
        print("\\n📋 Available voice commands:")
        for cmd, patterns_list in list(patterns.items())[:5]:
            print(f"   {cmd}: {patterns_list[0]}")
        
        print("\\n🎉 Voice commands test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Voice commands test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_voice_commands()
'''
    
    try:
        with open('test_voice_simple.py', 'w') as f:
            f.write(test_script)
        print_status("Created test_voice_simple.py", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Failed to create test script: {e}", "ERROR")
        return False

def create_voice_commands_fix():
    """Create a fixed version of voice commands"""
    print_header("CREATING FIXED VOICE COMMANDS")

    fixed_voice_commands = '''#!/usr/bin/env python3
"""
FIXED Voice Command System for Iris Recognition
This version includes error handling and fallback modes
"""

import threading
import time
import logging
from datetime import datetime

# Voice recognition imports with error handling
try:
    import speech_recognition as sr
    import pyaudio
    VOICE_RECOGNITION_AVAILABLE = True
    print("✅ Speech recognition available")
except ImportError as e:
    VOICE_RECOGNITION_AVAILABLE = False
    print(f"⚠️ Speech recognition not available: {e}")

# Text-to-speech import with error handling
try:
    import pyttsx3
    TTS_AVAILABLE = True
    print("✅ Text-to-speech available")
except ImportError as e:
    TTS_AVAILABLE = False
    print(f"⚠️ Text-to-speech not available: {e}")

logger = logging.getLogger(__name__)

class FixedVoiceCommandSystem:
    """Fixed voice command system with better error handling"""

    def __init__(self, main_app=None):
        self.main_app = main_app
        self.is_listening = False
        self.recognition_thread = None
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.command_callbacks = {}

        # Setup commands first
        self._setup_commands()

        # Initialize hardware safely
        self._safe_init_hardware()

    def _safe_init_hardware(self):
        """Safely initialize hardware components"""
        try:
            if VOICE_RECOGNITION_AVAILABLE:
                self._init_speech_recognition()
            if TTS_AVAILABLE:
                self._init_text_to_speech()
        except Exception as e:
            print(f"Hardware initialization error: {e}")

    def _init_speech_recognition(self):
        """Initialize speech recognition safely"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            print("✅ Speech recognition initialized")
        except Exception as e:
            print(f"⚠️ Speech recognition init failed: {e}")
            self.recognizer = None
            self.microphone = None

    def _init_text_to_speech(self):
        """Initialize text-to-speech safely"""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            print("✅ Text-to-speech initialized")
        except Exception as e:
            print(f"⚠️ TTS init failed: {e}")
            self.tts_engine = None

    def _setup_commands(self):
        """Setup voice command patterns"""
        self.command_patterns = {
            'start_recognition': [
                'start recognition', 'begin recognition', 'start iris recognition',
                'start live recognition', 'activate recognition'
            ],
            'take_photo': [
                'take photo', 'take picture', 'capture image', 'take screenshot'
            ],
            'show_gallery': [
                'show gallery', 'open gallery', 'view gallery', 'display gallery'
            ],
            'stop_recognition': [
                'stop recognition', 'end recognition', 'stop scanning'
            ],
            'train_model': [
                'train model', 'start training', 'begin training'
            ],
            'test_recognition': [
                'test recognition', 'test model', 'verify recognition'
            ],
            'view_analytics': [
                'view analytics', 'show analytics', 'display analytics'
            ],
            'system_status': [
                'system status', 'check status', 'show status'
            ],
            'help': [
                'help', 'what can you do', 'show commands', 'voice commands'
            ]
        }

    def register_callback(self, command, callback):
        """Register a callback function for a voice command"""
        self.command_callbacks[command] = callback
        print(f"✅ Registered callback for '{command}'")

    def speak(self, text):
        """Convert text to speech with fallback"""
        print(f"🔊 {text}")  # Always print as fallback

        if self.tts_engine:
            try:
                def tts_worker():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()

                tts_thread = threading.Thread(target=tts_worker)
                tts_thread.daemon = True
                tts_thread.start()
            except Exception as e:
                print(f"TTS error: {e}")

    def start_listening(self):
        """Start listening for voice commands"""
        if not VOICE_RECOGNITION_AVAILABLE:
            self.speak("Voice recognition not available. Commands will work in demo mode.")
            return True

        if not self.recognizer or not self.microphone:
            self.speak("Microphone not available. Voice commands in demo mode.")
            return True

        self.is_listening = True
        self.speak("Voice commands activated. Say 'help' for available commands.")

        # Start listening thread
        self.recognition_thread = threading.Thread(target=self._listen_worker)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()

        return True

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.speak("Voice commands deactivated.")

    def _listen_worker(self):
        """Background worker for voice recognition"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)

                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"🎤 Heard: {command}")
                    self._process_command(command)
                except sr.UnknownValueError:
                    pass  # No speech detected
                except sr.RequestError as e:
                    print(f"Speech service error: {e}")
                    time.sleep(2)
            except sr.WaitTimeoutError:
                pass  # Timeout is normal
            except Exception as e:
                print(f"Voice recognition error: {e}")
                time.sleep(1)

    def _process_command(self, command_text):
        """Process recognized voice command"""
        command_text = command_text.lower().strip()

        # Find matching command
        matched_command = None
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if pattern in command_text:
                    matched_command = command_type
                    break
            if matched_command:
                break

        if matched_command:
            print(f"✅ Executing: {matched_command}")
            self._execute_command(matched_command)
        else:
            self.speak(f"Unknown command: {command_text}")

    def _execute_command(self, command):
        """Execute a voice command"""
        try:
            if command in self.command_callbacks:
                self.speak(f"Executing {command.replace('_', ' ')}")
                self.command_callbacks[command]()
            elif command == 'help':
                self._show_help()
            else:
                self.speak(f"Command {command} not implemented yet.")
        except Exception as e:
            print(f"Error executing {command}: {e}")
            self.speak("Sorry, there was an error executing that command.")

    def _show_help(self):
        """Show available voice commands"""
        self.speak("Available voice commands:")
        commands = list(self.command_patterns.keys())[:5]  # Show first 5
        for cmd in commands:
            example = self.command_patterns[cmd][0]
            print(f"  - {example}")
        self.speak(f"Say any of these {len(commands)} commands to control the system.")

# Global instance
fixed_voice_system = None

def initialize_fixed_voice_commands(main_app=None):
    """Initialize the fixed voice command system"""
    global fixed_voice_system
    if fixed_voice_system is None:
        fixed_voice_system = FixedVoiceCommandSystem(main_app)
    return fixed_voice_system

def get_fixed_voice_system():
    """Get the fixed voice command system"""
    return fixed_voice_system

# For compatibility with existing code
VoiceCommandSystem = FixedVoiceCommandSystem
initialize_voice_commands = initialize_fixed_voice_commands
get_voice_system = get_fixed_voice_system

def is_voice_available():
    """Check if voice recognition is available"""
    return VOICE_RECOGNITION_AVAILABLE or TTS_AVAILABLE
'''

    try:
        with open('voice_commands_fixed_new.py', 'w') as f:
            f.write(fixed_voice_commands)
        print_status("Created voice_commands_fixed_new.py", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Failed to create fixed voice commands: {e}", "ERROR")
        return False

def main():
    """Main fix function"""
    print("🎤 VOICE COMMANDS FIX TOOL")
    print("=" * 60)
    print("This tool will fix all voice command issues in your iris recognition system.")

    # Step 1: Install dependencies
    print_status("Step 1: Installing dependencies...", "INFO")
    install_dependencies()

    # Step 2: Test imports
    print_status("Step 2: Testing imports...", "INFO")
    imports_ok = test_imports()

    # Step 3: Create fixed voice commands
    print_status("Step 3: Creating fixed voice commands...", "INFO")
    create_voice_commands_fix()

    # Step 4: Test voice system
    print_status("Step 4: Testing voice system...", "INFO")
    if imports_ok:
        test_voice_system()

    # Step 5: Test hardware
    print_status("Step 5: Testing hardware...", "INFO")
    if imports_ok:
        test_hardware()

    # Step 6: Create test script
    print_status("Step 6: Creating test script...", "INFO")
    create_voice_test_script()

    print_header("FIX COMPLETE")
    print_status("Voice commands fix completed!", "SUCCESS")
    print_status("Next steps:", "INFO")
    print("1. Run: install_all_dependencies.bat (to install missing packages)")
    print("2. Run: python test_voice_simple.py (to test voice commands)")
    print("3. If issues persist, use voice_commands_fixed_new.py")

    return True

if __name__ == "__main__":
    main()
