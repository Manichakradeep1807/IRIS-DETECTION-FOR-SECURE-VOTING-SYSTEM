@echo off
echo ========================================
echo VOICE COMMANDS DIAGNOSIS TOOL
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo.
echo Checking voice command dependencies...
echo.

echo Testing speech_recognition...
python -c "import speech_recognition; print('✅ speech_recognition: OK')" 2>nul || echo "❌ speech_recognition: MISSING"

echo Testing pyaudio...
python -c "import pyaudio; print('✅ pyaudio: OK')" 2>nul || echo "❌ pyaudio: MISSING"

echo Testing pyttsx3...
python -c "import pyttsx3; print('✅ pyttsx3: OK')" 2>nul || echo "❌ pyttsx3: MISSING"

echo.
echo Testing voice_commands module...
python -c "from voice_commands import VoiceCommandSystem; print('✅ voice_commands: OK')" 2>nul || echo "❌ voice_commands: FAILED"

echo.
echo ========================================
echo DIAGNOSIS COMPLETE
echo ========================================
echo.
echo If any dependencies are missing, run:
echo pip install SpeechRecognition pyttsx3 pyaudio
echo.
echo Or run: install_all_dependencies.bat
echo.
pause
