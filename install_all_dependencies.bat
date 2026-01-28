@echo off
echo ========================================
echo IRIS RECOGNITION - DEPENDENCY INSTALLER
echo ========================================
echo.
echo This will install all required dependencies for the iris recognition system
echo including voice commands support.
echo.
pause

echo Installing Python packages...
echo.

REM Core ML and CV packages
echo Installing TensorFlow...
pip install tensorflow>=2.10.0

echo Installing OpenCV...
pip install opencv-python>=4.5.0

echo Installing NumPy...
pip install numpy>=1.21.0

echo Installing Matplotlib...
pip install matplotlib>=3.5.0

echo Installing Scikit-learn...
pip install scikit-learn>=1.0.0

echo Installing Scikit-image...
pip install scikit-image>=0.19.0

echo Installing Pillow...
pip install Pillow>=8.0.0

echo Installing Albumentations...
pip install albumentations>=1.3.0

echo Installing Seaborn...
pip install seaborn>=0.11.0

echo Installing psutil...
pip install psutil>=5.8.0

REM Voice command packages
echo.
echo ========================================
echo INSTALLING VOICE COMMAND DEPENDENCIES
echo ========================================
echo.

echo Installing SpeechRecognition...
pip install SpeechRecognition>=3.10.0

echo Installing pyttsx3...
pip install pyttsx3>=2.90

echo Installing PyAudio (this might take a moment)...
pip install pyaudio>=0.2.11

echo.
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.
echo All dependencies have been installed.
echo You can now run the iris recognition system with voice commands.
echo.
pause
