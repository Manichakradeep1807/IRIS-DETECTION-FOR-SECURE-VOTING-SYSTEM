#!/usr/bin/env python3
"""
Fixed Voice Command System for Iris Recognition
Optimized version that doesn't hang on initialization
"""

import threading
import time
import logging
from datetime import datetime

# Voice recognition imports
try:
    import speech_recognition as sr
    import pyaudio
    VOICE_RECOGNITION_AVAILABLE = True
except ImportError:
    VOICE_RECOGNITION_AVAILABLE = False

# Text-to-speech import
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

logger = logging.getLogger(__name__)

class VoiceCommandSystem:
    """Fixed Voice command system for iris recognition"""
    
    def __init__(self, main_app=None):
        self.main_app = main_app
        self.is_listening = False
        self.recognition_thread = None
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        
        # Voice command callbacks
        self.command_callbacks = {}
        
        # Initialize components (non-blocking)
        self._setup_commands()
        self._initialize_components_async()
    
    def _initialize_components_async(self):
        """Initialize components in background to avoid hanging"""
        def init_worker():
            self._initialize_speech_recognition()
            self._initialize_text_to_speech()
        
        init_thread = threading.Thread(target=init_worker)
        init_thread.daemon = True
        init_thread.start()
    
    def _initialize_speech_recognition(self):
        """Initialize speech recognition components"""
        if not VOICE_RECOGNITION_AVAILABLE:
            logger.warning("Speech recognition not available")
            return False
        
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Quick ambient noise adjustment (reduced time)
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            logger.info("Speech recognition initialized")
            return True
            
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return False
    
    def _initialize_text_to_speech(self):
        """Initialize text-to-speech engine"""
        if not TTS_AVAILABLE:
            logger.warning("Text-to-speech not available")
            return False
        
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            logger.info("Text-to-speech initialized")
            return True
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return False
    
    def _setup_commands(self):
        """Setup voice command mappings"""
        self.command_patterns = {
            # Core commands
            'start_recognition': ['start recognition', 'begin recognition', 'start iris recognition'],
            'take_photo': ['take photo', 'take picture', 'capture image'],
            'show_gallery': ['show gallery', 'open gallery', 'view gallery'],
            'stop_recognition': ['stop recognition', 'end recognition', 'stop scanning'],
            'train_model': ['train model', 'start training', 'begin training'],
            'test_recognition': ['test recognition', 'test model', 'verify recognition'],
            'view_analytics': ['view analytics', 'show analytics', 'display analytics'],
            'system_status': ['system status', 'check status', 'show status'],
            'upload_dataset': ['upload dataset', 'load dataset', 'import dataset'],
            'open_settings': ['open settings', 'show settings', 'configure system'],
            'exit_application': ['exit application', 'close application', 'quit application'],
            'voice_status': ['voice status', 'voice commands status', 'check voice'],
            
            # NEW: Enhanced commands
            'clear_console': ['clear console', 'clear screen', 'clear output'],
            'refresh_system': ['refresh system', 'reload system', 'restart system'],
            'save_data': ['save data', 'backup data', 'export data'],
            'load_data': ['load data', 'restore data', 'import data'],
            'model_info': ['model information', 'model details', 'show model'],
            'check_performance': ['check performance', 'performance metrics', 'system performance'],
            'check_memory': ['check memory', 'memory usage', 'memory status'],
            'camera_status': ['camera status', 'check camera', 'camera info'],
            'database_status': ['database status', 'check database', 'database info'],
            'show_logs': ['show logs', 'view logs', 'display logs'],
            'version_info': ['version information', 'software version', 'system version'],
            'current_time': ['current time', 'what time is it', 'show time'],
            'minimize_window': ['minimize window', 'minimize application', 'hide window'],
            'maximize_window': ['maximize window', 'maximize application', 'fullscreen mode'],
            'change_theme': ['change theme', 'switch theme', 'dark theme'],
            'change_language': ['change language', 'switch language', 'language settings'],
            'help': ['help', 'show commands', 'voice commands', 'list commands']
        }
    
    def register_callback(self, command, callback):
        """Register a callback function for a voice command"""
        self.command_callbacks[command] = callback
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.tts_engine:
            print(f"🔊 {text}")
            return
        
        try:
            def tts_worker():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            tts_thread = threading.Thread(target=tts_worker)
            tts_thread.daemon = True
            tts_thread.start()
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"🔊 {text}")
    
    def start_listening(self):
        """Start listening for voice commands"""
        if not VOICE_RECOGNITION_AVAILABLE or not self.recognizer:
            self.speak("Voice recognition is not available.")
            return False
        
        if self.is_listening:
            return True
        
        self.is_listening = True
        
        # Start listening thread
        self.recognition_thread = threading.Thread(target=self._listen_worker)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        self.speak("Voice commands activated.")
        logger.info("Voice command system started")
        return True
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        if not self.is_listening:
            return
        
        self.is_listening = False
        self.speak("Voice commands deactivated.")
        logger.info("Voice command system stopped")
    
    def _listen_worker(self):
        """Background worker for voice recognition"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    logger.info(f"Voice command: {command}")
                    self._process_command(command)
                    
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    logger.error(f"Speech service error: {e}")
                    time.sleep(2)
                
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                logger.error(f"Voice recognition error: {e}")
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
            logger.info(f"Executing: {matched_command}")
            self._execute_command(matched_command, command_text)
        else:
            self.speak(f"Unknown command: {command_text}")
    
    def _execute_command(self, command, original_text):
        """Execute a recognized voice command"""
        try:
            if command in self.command_callbacks:
                self.speak(f"Executing {command.replace('_', ' ')}")
                self.command_callbacks[command]()
            else:
                self.speak(f"Command {command} is not implemented yet.")
                
        except Exception as e:
            logger.error(f"Error executing {command}: {e}")
            self.speak("Sorry, there was an error executing that command.")

# Global voice command system instance
voice_system = None

def initialize_voice_commands(main_app=None):
    """Initialize the global voice command system"""
    global voice_system
    if voice_system is None:
        voice_system = VoiceCommandSystem(main_app)
    return voice_system

def get_voice_system():
    """Get the global voice command system"""
    return voice_system

def is_voice_available():
    """Check if voice recognition is available"""
    return VOICE_RECOGNITION_AVAILABLE and TTS_AVAILABLE
