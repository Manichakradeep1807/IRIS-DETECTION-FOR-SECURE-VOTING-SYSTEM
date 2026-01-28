@echo off
echo ========================================
echo COMPLETE IRIS RECOGNITION PROJECT FIX
echo ========================================
echo.
echo This will install ALL required dependencies for your project.
echo This may take 10-15 minutes depending on your internet speed.
echo.
echo WHAT WILL BE INSTALLED:
echo - TensorFlow (AI/Machine Learning)
echo - OpenCV (Computer Vision)
echo - NumPy, Matplotlib (Data Processing)
echo - SpeechRecognition, PyAudio, pyttsx3 (Voice Commands)
echo - All other required packages
echo.
pause

echo.
echo ========================================
echo STEP 1: UPDATING PIP
echo ========================================
echo.
python -m pip install --upgrade pip

echo.
echo ========================================
echo STEP 2: INSTALLING CORE ML/AI PACKAGES
echo ========================================
echo.

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

echo.
echo ========================================
echo STEP 3: INSTALLING VOICE COMMAND PACKAGES
echo ========================================
echo.

echo Installing SpeechRecognition...
pip install SpeechRecognition>=3.10.0

echo Installing pyttsx3...
pip install pyttsx3>=2.90

echo Installing PyAudio (this may take longer)...
pip install pyaudio>=0.2.11

echo.
echo ========================================
echo STEP 4: INSTALLING ADDITIONAL PACKAGES
echo ========================================
echo.

echo Installing psutil...
pip install psutil>=5.8.0

echo Installing seaborn...
pip install seaborn>=0.11.0

echo Installing albumentations...
pip install albumentations>=1.3.0

echo.
echo ========================================
echo STEP 5: TESTING INSTALLATION
echo ========================================
echo.

echo Testing TensorFlow...
python -c "import tensorflow as tf; print(f'✅ TensorFlow {tf.__version__} installed successfully')" || echo "❌ TensorFlow installation failed"

echo Testing OpenCV...
python -c "import cv2; print(f'✅ OpenCV {cv2.__version__} installed successfully')" || echo "❌ OpenCV installation failed"

echo Testing Voice Commands...
python -c "import speech_recognition, pyttsx3, pyaudio; print('✅ Voice command packages installed successfully')" || echo "❌ Voice command packages installation failed"

echo.
echo ========================================
echo STEP 6: TESTING PROJECT
echo ========================================
echo.

echo Testing project imports...
python -c "from voice_commands import VoiceCommandSystem; print('✅ Voice commands working')" || echo "❌ Voice commands need fixing"

echo Testing Main.py imports...
python -c "import sys; sys.path.append('.'); exec(open('Main.py').read().split('main = tk.Tk()')[0]); print('✅ Main.py imports working')" || echo "❌ Main.py has import issues"

echo.
echo ========================================
echo INSTALLATION COMPLETE!
echo ========================================
echo.
echo 🎉 All packages have been installed!
echo.
echo 🚀 TO RUN YOUR PROJECT:
echo    python Main.py
echo.
echo 🎤 VOICE COMMANDS AVAILABLE:
echo    - "Start recognition"
echo    - "Take photo"
echo    - "Show gallery"
echo    - "Train model"
echo    - "Help"
echo.
echo 📊 PROJECT FEATURES:
echo    ✅ High-accuracy iris recognition (98%+ target)
echo    ✅ Live camera recognition
echo    ✅ Voice command control
echo    ✅ Iris image gallery
echo    ✅ Analytics dashboard
echo    ✅ Modern GUI with dark theme
echo.
echo If you encounter any issues, run:
echo    diagnose_project.bat
echo.
pause
