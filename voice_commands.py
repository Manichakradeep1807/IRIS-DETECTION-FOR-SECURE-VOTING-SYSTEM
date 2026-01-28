#!/usr/bin/env python3
"""
Voice Command System for Iris Recognition
Supports voice commands: "Start recognition", "Take photo", "Show gallery"
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

# Language support
try:
    from language_manager import get_text
    LANGUAGE_SUPPORT = True
except ImportError:
    LANGUAGE_SUPPORT = False

logger = logging.getLogger(__name__)

class VoiceCommandSystem:
    """Voice command system for iris recognition"""
    
    def __init__(self, main_app=None):
        self.main_app = main_app
        self.is_listening = False
        self.recognition_thread = None
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None

        # Voice command callbacks
        self.command_callbacks = {}

        # Initialize components (setup commands first, then try hardware)
        self._setup_commands()

        # Initialize hardware in background to avoid hanging
        self._init_hardware_async()

    def _init_hardware_async(self):
        """Initialize hardware components in background thread"""
        def init_worker():
            try:
                self._initialize_speech_recognition()
                self._initialize_text_to_speech()
            except Exception as e:
                logger.error("Hardware initialization error: {}".format(e))

        # Run in background thread to avoid blocking
        init_thread = threading.Thread(target=init_worker)
        init_thread.daemon = True
        init_thread.start()

    def _initialize_speech_recognition(self):
        """Initialize speech recognition components"""
        if not VOICE_RECOGNITION_AVAILABLE:
            logger.warning("Speech recognition not available - install SpeechRecognition and pyaudio")
            return False

        try:
            self.recognizer = sr.Recognizer()

            # Try to initialize microphone without hanging
            try:
                self.microphone = sr.Microphone()
                # Quick ambient noise adjustment to avoid hanging
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                logger.info("Speech recognition initialized successfully")
                return True
            except Exception as mic_error:
                logger.warning("Microphone initialization failed: {}".format(mic_error))
                # Create a dummy microphone for testing
                self.microphone = None
                logger.info("Speech recognition initialized in fallback mode")
                return True

        except Exception as e:
            logger.error("Error initializing speech recognition: {}".format(e))
            return False
    
    def _initialize_text_to_speech(self):
        """Initialize text-to-speech engine"""
        if not TTS_AVAILABLE:
            logger.warning("Text-to-speech not available - install pyttsx3")
            return False

        try:
            # Try to initialize TTS with timeout protection
            try:
                self.tts_engine = pyttsx3.init()

                # Configure TTS settings quickly
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.8)

                logger.info("Text-to-speech initialized successfully")
                return True

            except Exception as tts_error:
                logger.warning("TTS initialization failed: {}".format(tts_error))
                # Set to None for fallback to print
                self.tts_engine = None
                logger.info("TTS initialized in fallback mode (print only)")
                return True

        except Exception as e:
            logger.error("Error initializing text-to-speech: {}".format(e))
            self.tts_engine = None
            return False
    
    def _setup_commands(self):
        """Setup voice command mappings - ENHANCED WITH 25+ COMMAND CATEGORIES"""
        # Define command patterns and their callbacks
        self.command_patterns = {
            # Start recognition commands
            'start_recognition': [
                'start recognition', 'begin recognition', 'start iris recognition',
                'start live recognition', 'begin iris scan', 'start scanning',
                'activate recognition', 'launch recognition', 'turn on recognition',
                'enable recognition', 'commence recognition', 'initiate scanning'
            ],

            # Take photo commands
            'take_photo': [
                'take photo', 'take picture', 'capture image', 'take screenshot',
                'save image', 'capture photo', 'snap photo', 'capture now',
                'take a shot', 'grab image', 'save picture', 'capture frame'
            ],

            # Show gallery commands
            'show_gallery': [
                'show gallery', 'open gallery', 'view gallery', 'display gallery',
                'show images', 'view images', 'open images', 'display images',
                'browse gallery', 'gallery view', 'image browser', 'photo gallery'
            ],

            # Stop/Exit commands
            'stop_recognition': [
                'stop recognition', 'end recognition', 'stop scanning', 'quit recognition',
                'exit recognition', 'halt recognition', 'pause recognition',
                'disable recognition', 'turn off recognition', 'cease recognition'
            ],

            # Train model commands
            'train_model': [
                'train model', 'start training', 'begin training', 'train neural network',
                'train cnn', 'load model', 'create model', 'build model',
                'train algorithm', 'start learning', 'neural training', 'model training'
            ],

            # Test recognition commands
            'test_recognition': [
                'test recognition', 'test model', 'verify recognition', 'check recognition',
                'test iris', 'validate model', 'run test', 'recognition test',
                'model validation', 'accuracy test', 'performance test'
            ],

            # View analytics commands
            'view_analytics': [
                'view analytics', 'show analytics', 'display analytics', 'show statistics',
                'view stats', 'show metrics', 'display metrics', 'analytics dashboard',
                'performance metrics', 'system analytics', 'data visualization'
            ],

            # System status commands
            'system_status': [
                'system status', 'check status', 'show status', 'system health',
                'performance status', 'check system', 'system info', 'health check',
                'status report', 'system diagnostics', 'performance check'
            ],

            # Upload dataset commands
            'upload_dataset': [
                'upload dataset', 'load dataset', 'import dataset', 'add dataset',
                'select dataset', 'browse dataset', 'choose dataset', 'dataset upload',
                'import data', 'load training data', 'add training images'
            ],

            # Settings commands
            'open_settings': [
                'open settings', 'show settings', 'configure system', 'system settings',
                'preferences', 'configuration', 'setup', 'options',
                'system config', 'adjust settings', 'modify settings'
            ],

            # Exit application commands
            'exit_application': [
                'exit application', 'close application', 'quit application', 'shutdown system',
                'exit program', 'close program', 'terminate application', 'shut down',
                'quit system', 'close system', 'exit now', 'goodbye'
            ],

            # Voice control commands
            'voice_status': [
                'voice status', 'voice commands status', 'check voice', 'voice system status',
                'voice info', 'microphone status', 'speech status', 'voice check'
            ],

            # NEW: Clear console commands
            'clear_console': [
                'clear console', 'clear screen', 'clear output', 'clean console',
                'clear text', 'reset console', 'clear display', 'clean screen'
            ],

            # NEW: Refresh system commands
            'refresh_system': [
                'refresh system', 'reload system', 'restart system', 'refresh interface',
                'update system', 'reload interface', 'system refresh', 'refresh all'
            ],

            # NEW: Save data commands
            'save_data': [
                'save data', 'save information', 'backup data', 'export data',
                'save results', 'store data', 'save configuration', 'backup system'
            ],

            # NEW: Load data commands
            'load_data': [
                'load data', 'import data', 'restore data', 'load backup',
                'import configuration', 'restore backup', 'load settings'
            ],

            # NEW: Model information commands
            'model_info': [
                'model information', 'model details', 'show model', 'model stats',
                'model summary', 'neural network info', 'architecture info', 'model parameters'
            ],

            # NEW: Performance commands
            'check_performance': [
                'check performance', 'performance metrics', 'system performance',
                'speed test', 'benchmark system', 'performance analysis', 'efficiency check'
            ],

            # NEW: Memory commands
            'check_memory': [
                'check memory', 'memory usage', 'memory status', 'ram usage',
                'memory info', 'system memory', 'memory statistics'
            ],

            # NEW: Camera commands
            'camera_status': [
                'camera status', 'check camera', 'camera info', 'webcam status',
                'camera test', 'video status', 'camera check', 'camera settings'
            ],

            # NEW: Database commands
            'database_status': [
                'database status', 'check database', 'database info', 'db status',
                'database health', 'data storage', 'database check'
            ],

            # NEW: Log commands
            'show_logs': [
                'show logs', 'view logs', 'display logs', 'system logs',
                'error logs', 'activity logs', 'log files', 'log history'
            ],

            # NEW: Version commands
            'version_info': [
                'version information', 'software version', 'system version', 'version details',
                'about system', 'version number', 'build info', 'release info'
            ],

            # NEW: Time/Date commands
            'current_time': [
                'current time', 'what time is it', 'show time', 'time now',
                'current date', 'today date', 'date and time', 'system time'
            ],

            # NEW: Minimize/Maximize commands
            'minimize_window': [
                'minimize window', 'minimize application', 'hide window', 'minimize app',
                'reduce window', 'minimize interface', 'hide interface'
            ],

            'maximize_window': [
                'maximize window', 'maximize application', 'fullscreen mode', 'maximize app',
                'expand window', 'full screen', 'maximize interface'
            ],

            # NEW: Theme commands
            'change_theme': [
                'change theme', 'switch theme', 'dark theme', 'light theme',
                'theme settings', 'color scheme', 'appearance settings'
            ],

            # NEW: Language commands
            'change_language': [
                'change language', 'switch language', 'language settings', 'set language',
                'language options', 'language preferences', 'locale settings'
            ],

            # Help commands (enhanced)
            'help': [
                'help', 'what can you do', 'show commands', 'voice commands',
                'list commands', 'available commands', 'command list', 'help me',
                'assistance', 'guide', 'instructions', 'how to use', 'voice help'
            ]
        }
    
    def register_callback(self, command, callback):
        """Register a callback function for a voice command"""
        self.command_callbacks[command] = callback
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.tts_engine:
            print("🔊 {}".format(text))  # Fallback to print
            return
        
        try:
            # Run TTS in separate thread to avoid blocking
            def tts_worker():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            tts_thread = threading.Thread(target=tts_worker)
            tts_thread.daemon = True
            tts_thread.start()
            
        except Exception as e:
            logger.error("Error in text-to-speech: {}".format(e))
            print("🔊 {}".format(text))  # Fallback to print
    
    def _get_localized_text(self, key, default):
        """Get localized text if language support is available"""
        if LANGUAGE_SUPPORT:
            return get_text(key, default)
        return default
    
    def start_listening(self):
        """Start listening for voice commands"""
        if not VOICE_RECOGNITION_AVAILABLE or not self.recognizer:
            self.speak("Voice recognition is not available. Please install required packages.")
            return False

        if not self.microphone:
            self.speak("Microphone is not available. Voice commands will work in demo mode.")
            # Still return True to show the commands in the console
            return True

        if self.is_listening:
            return True

        self.is_listening = True

        # Start listening thread only if microphone is available
        if self.microphone:
            self.recognition_thread = threading.Thread(target=self._listen_worker)
            self.recognition_thread.daemon = True
            self.recognition_thread.start()

        # Announce voice commands are active
        welcome_msg = self._get_localized_text("voice_welcome", "Voice commands activated. Say 'help' for available commands.")
        self.speak(welcome_msg)

        logger.info("Voice command system started")
        return True
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        if not self.is_listening:
            return
        
        self.is_listening = False
        
        # Announce voice commands are stopped
        goodbye_msg = self._get_localized_text("voice_goodbye", "Voice commands deactivated.")
        self.speak(goodbye_msg)
        
        logger.info("Voice command system stopped")
    
    def _listen_worker(self):
        """Background worker for voice recognition"""
        while self.is_listening:
            try:
                # Listen for audio
                with self.microphone as source:
                    # Listen with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Recognize speech
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    logger.info("Voice command recognized: {}".format(command))
                    
                    # Process the command
                    self._process_command(command)
                    
                except sr.UnknownValueError:
                    # No speech detected - this is normal
                    pass
                except sr.RequestError as e:
                    logger.error("Speech recognition service error: {}".format(e))
                    time.sleep(2)  # Wait before retrying
                
            except sr.WaitTimeoutError:
                # Timeout - this is normal, continue listening
                pass
            except Exception as e:
                logger.error("Error in voice recognition worker: {}".format(e))
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
            logger.info("Executing voice command: {}".format(matched_command))
            self._execute_command(matched_command, command_text)
        else:
            # Unknown command
            unknown_msg = self._get_localized_text("voice_unknown", "Unknown command: {}".format(command_text))
            self.speak(unknown_msg)
    
    def _execute_command(self, command, original_text):
        """Execute a recognized voice command - ENHANCED WITH ALL NEW COMMANDS"""
        try:
            # Core recognition commands
            if command == 'start_recognition':
                self._handle_start_recognition()
            elif command == 'take_photo':
                self._handle_take_photo()
            elif command == 'show_gallery':
                self._handle_show_gallery()
            elif command == 'stop_recognition':
                self._handle_stop_recognition()
            elif command == 'train_model':
                self._handle_train_model()
            elif command == 'test_recognition':
                self._handle_test_recognition()
            elif command == 'view_analytics':
                self._handle_view_analytics()
            elif command == 'system_status':
                self._handle_system_status()
            elif command == 'upload_dataset':
                self._handle_upload_dataset()
            elif command == 'open_settings':
                self._handle_open_settings()
            elif command == 'exit_application':
                self._handle_exit_application()
            elif command == 'voice_status':
                self._handle_voice_status()

            # NEW: System utility commands
            elif command == 'clear_console':
                self._handle_clear_console()
            elif command == 'refresh_system':
                self._handle_refresh_system()
            elif command == 'save_data':
                self._handle_save_data()
            elif command == 'load_data':
                self._handle_load_data()
            elif command == 'model_info':
                self._handle_model_info()
            elif command == 'check_performance':
                self._handle_check_performance()
            elif command == 'check_memory':
                self._handle_check_memory()
            elif command == 'camera_status':
                self._handle_camera_status()
            elif command == 'database_status':
                self._handle_database_status()
            elif command == 'show_logs':
                self._handle_show_logs()
            elif command == 'version_info':
                self._handle_version_info()
            elif command == 'current_time':
                self._handle_current_time()
            elif command == 'minimize_window':
                self._handle_minimize_window()
            elif command == 'maximize_window':
                self._handle_maximize_window()
            elif command == 'change_theme':
                self._handle_change_theme()
            elif command == 'change_language':
                self._handle_change_language()
            elif command == 'help':
                self._handle_help()
            else:
                self.speak("Command {} is not implemented yet.".format(command))

        except Exception as e:
            logger.error("Error executing command {}: {e}".format(command))
            error_msg = self._get_localized_text("voice_error", "Sorry, there was an error executing that command.")
            self.speak(error_msg)
    
    def _handle_start_recognition(self):
        """Handle start recognition command"""
        if 'start_recognition' in self.command_callbacks:
            self.speak("Starting iris recognition...")
            self.command_callbacks['start_recognition']()
        else:
            self.speak("Start recognition function is not available.")
    
    def _handle_take_photo(self):
        """Handle take photo command"""
        if 'take_photo' in self.command_callbacks:
            self.speak("Taking photo...")
            self.command_callbacks['take_photo']()
        else:
            self.speak("Photo capture function is not available.")
    
    def _handle_show_gallery(self):
        """Handle show gallery command"""
        if 'show_gallery' in self.command_callbacks:
            self.speak("Opening iris gallery...")
            self.command_callbacks['show_gallery']()
        else:
            self.speak("Gallery function is not available.")
    
    def _handle_stop_recognition(self):
        """Handle stop recognition command"""
        if 'stop_recognition' in self.command_callbacks:
            self.speak("Stopping recognition...")
            self.command_callbacks['stop_recognition']()
        else:
            self.speak("Stop function is not available.")
    
    def _handle_train_model(self):
        """Handle train model command"""
        if 'train_model' in self.command_callbacks:
            self.speak("Starting model training...")
            self.command_callbacks['train_model']()
        else:
            self.speak("Model training function is not available.")

    def _handle_test_recognition(self):
        """Handle test recognition command"""
        if 'test_recognition' in self.command_callbacks:
            self.speak("Starting recognition test...")
            self.command_callbacks['test_recognition']()
        else:
            self.speak("Test recognition function is not available.")



    def _handle_system_status(self):
        """Handle system status command"""
        if 'system_status' in self.command_callbacks:
            self.speak("Checking system status...")
            self.command_callbacks['system_status']()
        else:
            self.speak("System status function is not available.")

    def _handle_upload_dataset(self):
        """Handle upload dataset command"""
        if 'upload_dataset' in self.command_callbacks:
            self.speak("Opening dataset upload...")
            self.command_callbacks['upload_dataset']()
        else:
            self.speak("Dataset upload function is not available.")

    def _handle_open_settings(self):
        """Handle open settings command"""
        if 'open_settings' in self.command_callbacks:
            self.speak("Opening system settings...")
            self.command_callbacks['open_settings']()
        else:
            self.speak("Settings function is not available.")

    def _handle_exit_application(self):
        """Handle exit application command"""
        if 'exit_application' in self.command_callbacks:
            self.speak("Closing application...")
            self.command_callbacks['exit_application']()
        else:
            self.speak("Exit function is not available.")

    def _handle_voice_status(self):
        """Handle voice status command"""
        status = "Voice commands are active and listening" if self.is_listening else "Voice commands are inactive"
        self.speak("Voice system status: {}".format(status))

    def _handle_clear_console(self):
        """Handle clear console command"""
        if 'clear_console' in self.command_callbacks:
            self.speak("Clearing console...")
            self.command_callbacks['clear_console']()
        else:
            self.speak("Clear console function is not available.")

    def _handle_refresh_system(self):
        """Handle refresh system command"""
        if 'refresh_system' in self.command_callbacks:
            self.speak("Refreshing system...")
            self.command_callbacks['refresh_system']()
        else:
            self.speak("System refresh function is not available.")

    def _handle_save_data(self):
        """Handle save data command"""
        if 'save_data' in self.command_callbacks:
            self.speak("Saving system data...")
            self.command_callbacks['save_data']()
        else:
            self.speak("Save data function is not available.")

    def _handle_load_data(self):
        """Handle load data command"""
        if 'load_data' in self.command_callbacks:
            self.speak("Loading system data...")
            self.command_callbacks['load_data']()
        else:
            self.speak("Load data function is not available.")

    def _handle_model_info(self):
        """Handle model information command"""
        if 'model_info' in self.command_callbacks:
            self.speak("Displaying model information...")
            self.command_callbacks['model_info']()
        else:
            self.speak("Model information function is not available.")

    def _handle_check_performance(self):
        """Handle check performance command"""
        if 'check_performance' in self.command_callbacks:
            self.speak("Checking system performance...")
            self.command_callbacks['check_performance']()
        else:
            self.speak("Performance check function is not available.")

    def _handle_check_memory(self):
        """Handle check memory command"""
        if 'check_memory' in self.command_callbacks:
            self.speak("Checking memory usage...")
            self.command_callbacks['check_memory']()
        else:
            self.speak("Memory check function is not available.")

    def _handle_camera_status(self):
        """Handle camera status command"""
        if 'camera_status' in self.command_callbacks:
            self.speak("Checking camera status...")
            self.command_callbacks['camera_status']()
        else:
            self.speak("Camera status function is not available.")

    def _handle_database_status(self):
        """Handle database status command"""
        if 'database_status' in self.command_callbacks:
            self.speak("Checking database status...")
            self.command_callbacks['database_status']()
        else:
            self.speak("Database status function is not available.")

    def _handle_show_logs(self):
        """Handle show logs command"""
        if 'show_logs' in self.command_callbacks:
            self.speak("Displaying system logs...")
            self.command_callbacks['show_logs']()
        else:
            self.speak("Show logs function is not available.")

    def _handle_version_info(self):
        """Handle version information command"""
        if 'version_info' in self.command_callbacks:
            self.speak("Displaying version information...")
            self.command_callbacks['version_info']()
        else:
            self.speak("Version information function is not available.")

    def _handle_current_time(self):
        """Handle current time command"""
        if 'current_time' in self.command_callbacks:
            self.speak("Displaying current time...")
            self.command_callbacks['current_time']()
        else:
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p on %B %d, %Y")
            self.speak("The current time is {}".format(current_time))

    def _handle_minimize_window(self):
        """Handle minimize window command"""
        if 'minimize_window' in self.command_callbacks:
            self.speak("Minimizing window...")
            self.command_callbacks['minimize_window']()
        else:
            self.speak("Minimize window function is not available.")

    def _handle_maximize_window(self):
        """Handle maximize window command"""
        if 'maximize_window' in self.command_callbacks:
            self.speak("Maximizing window...")
            self.command_callbacks['maximize_window']()
        else:
            self.speak("Maximize window function is not available.")

    def _handle_change_theme(self):
        """Handle change theme command"""
        if 'change_theme' in self.command_callbacks:
            self.speak("Changing theme...")
            self.command_callbacks['change_theme']()
        else:
            self.speak("Theme change function is not available.")

    def _handle_change_language(self):
        """Handle change language command"""
        if 'change_language' in self.command_callbacks:
            self.speak("Changing language...")
            self.command_callbacks['change_language']()
        else:
            self.speak("Language change function is not available.")

    def _handle_help(self):
        """Handle help command - ENHANCED WITH ALL NEW COMMANDS"""
        help_text = """Available voice commands:

        RECOGNITION COMMANDS:
        Start recognition - Begin iris scanning
        Stop recognition - End scanning
        Test recognition - Test iris recognition
        Take photo - Capture current image
        Show gallery - Open image gallery

        MODEL COMMANDS:
        Train model - Start model training
        View analytics - Show system analytics
        Model information - Display model details

        SYSTEM COMMANDS:
        System status - Check system health
        Check performance - System performance metrics
        Check memory - Memory usage information
        Camera status - Check camera availability
        Database status - Check database health
        Upload dataset - Load training data

        UTILITY COMMANDS:
        Clear console - Clear system output
        Refresh system - Reload system interface
        Save data - Backup system data
        Load data - Restore system data
        Show logs - Display system logs
        Version information - Software version details
        Current time - Display current date and time

        INTERFACE COMMANDS:
        Open settings - Configure system
        Minimize window - Minimize application
        Maximize window - Maximize application
        Change theme - Switch color theme
        Change language - Change system language

        VOICE COMMANDS:
        Voice status - Check voice system
        Help - Show this help
        Exit application - Close the program"""

        self.speak(help_text)

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
