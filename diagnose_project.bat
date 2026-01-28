@echo off
echo ========================================
echo IRIS RECOGNITION PROJECT DIAGNOSIS
echo ========================================
echo.
echo Checking if your project is ready to run...
echo.

echo 📁 CHECKING PROJECT FILES...
echo.

REM Check essential files
if exist "Main.py" (
    echo ✅ Main.py: Found
) else (
    echo ❌ Main.py: Missing
)

if exist "voice_commands.py" (
    echo ✅ voice_commands.py: Found
) else (
    echo ❌ voice_commands.py: Missing
)

if exist "requirements.txt" (
    echo ✅ requirements.txt: Found
) else (
    echo ❌ requirements.txt: Missing
)

REM Check directories
if exist "model" (
    echo ✅ model/: Found
) else (
    echo ❌ model/: Missing
)

if exist "captured_iris" (
    echo ✅ captured_iris/: Found
) else (
    echo ❌ captured_iris/: Missing
)

if exist "sample_dataset" (
    echo ✅ sample_dataset/: Found
) else (
    echo ❌ sample_dataset/: Missing
)

echo.
echo 📦 CHECKING PYTHON PACKAGES...
echo.

REM Check Python packages
python -c "import tkinter; print('✅ Tkinter: Available')" 2>nul || echo "❌ Tkinter: Missing"
python -c "import numpy; print('✅ NumPy: Available')" 2>nul || echo "❌ NumPy: Missing"
python -c "import cv2; print('✅ OpenCV: Available')" 2>nul || echo "❌ OpenCV: Missing"
python -c "import matplotlib; print('✅ Matplotlib: Available')" 2>nul || echo "❌ Matplotlib: Missing"
python -c "import tensorflow; print('✅ TensorFlow: Available')" 2>nul || echo "❌ TensorFlow: Missing"
python -c "import speech_recognition; print('✅ SpeechRecognition: Available')" 2>nul || echo "❌ SpeechRecognition: Missing"
python -c "import pyttsx3; print('✅ pyttsx3: Available')" 2>nul || echo "❌ pyttsx3: Missing"
python -c "import pyaudio; print('✅ PyAudio: Available')" 2>nul || echo "❌ PyAudio: Missing"

echo.
echo 🎤 CHECKING VOICE COMMANDS...
echo.

python -c "from voice_commands import VoiceCommandSystem; vs = VoiceCommandSystem(); print('✅ Voice commands: Working'); print(f'✅ Found {len(vs.command_patterns)} command patterns')" 2>nul || echo "❌ Voice commands: Failed"

echo.
echo 🧠 CHECKING MODEL FILES...
echo.

if exist "model\X.txt.npy" (
    echo ✅ Training data X: Found
) else (
    echo ❌ Training data X: Missing
)

if exist "model\Y.txt.npy" (
    echo ✅ Training data Y: Found
) else (
    echo ❌ Training data Y: Missing
)

if exist "model\model.json" (
    echo ✅ Model file: Found
) else (
    echo ❌ Model file: Missing
)

echo.
echo ========================================
echo DIAGNOSIS COMPLETE
echo ========================================
echo.

REM Try to run a quick Python test
echo Running comprehensive Python test...
python quick_project_test.py 2>nul

echo.
echo 🚀 TO RUN YOUR PROJECT:
echo    python Main.py
echo.
echo 🔧 IF ISSUES FOUND:
echo    1. Run: install_all_dependencies.bat
echo    2. Run: pip install -r requirements.txt
echo    3. Check camera and microphone connections
echo.
pause
