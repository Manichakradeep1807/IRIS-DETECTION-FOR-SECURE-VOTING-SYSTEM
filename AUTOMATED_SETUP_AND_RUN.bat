@echo off
title Iris Recognition Project - Automated Setup and Run
color 0A

echo ========================================
echo    IRIS RECOGNITION PROJECT SETUP
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)
echo ✅ Python found!

echo.
echo [2/5] Installing required packages...
echo This may take a few minutes...
echo.

pip install --upgrade pip
pip install tensorflow>=2.10.0
pip install opencv-python>=4.5.0
pip install numpy>=1.21.0
pip install matplotlib>=3.5.0
pip install scikit-learn>=1.0.0
pip install scikit-image>=0.19.0
pip install pyttsx3>=2.90
pip install Pillow>=8.0.0
pip install albumentations>=1.3.0
pip install seaborn>=0.11.0
pip install psutil>=5.8.0

echo.
echo [3/5] Verifying installation...
python -c "import tensorflow, cv2, numpy, matplotlib; print('✅ Core packages verified!')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Some packages may not be installed correctly
    echo Continuing anyway...
)

echo.
echo [4/5] Checking project structure...
if not exist "Main.py" (
    echo ERROR: Main.py not found! Make sure you're in the correct directory.
    pause
    exit /b 1
)
echo ✅ Project files found!

echo.
echo [5/5] Starting Iris Recognition System...
echo.
echo ========================================
echo    LAUNCHING APPLICATION...
echo ========================================
echo.
echo 🎯 QUICK START GUIDE:
echo 1. Click "🧠 TRAIN MODEL" first (creates sample data automatically)
echo 2. Click "🔍 TEST RECOGNITION" to test with sample images
echo 3. Click "📹 LIVE RECOGNITION" for real-time recognition
echo 4. Click "🖼️ IRIS GALLERY" to view captured images
echo.
echo Press any key to launch the application...
pause >nul

python Main.py

echo.
echo Application closed.
pause
