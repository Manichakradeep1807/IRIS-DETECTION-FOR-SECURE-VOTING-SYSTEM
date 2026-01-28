@echo off
echo ========================================
echo Iris Recognition Deep Learning Setup
echo ========================================
echo.
echo This script will set up the full deep learning environment
echo for the Iris Recognition system using Python 3.11
echo.

REM Check if Python 3.11 is available
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.11 is not installed!
    echo.
    echo Please install Python 3.11 from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Found Python 3.11! Setting up environment...
echo.

REM Create virtual environment
echo Creating virtual environment...
py -3.11 -m venv iris_env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call iris_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing deep learning packages...
echo This may take several minutes...
pip install numpy==1.24.3
pip install matplotlib==3.7.2
pip install opencv-python==4.8.1.78
pip install tensorflow==2.13.0
pip install keras==2.13.1
pip install scikit-image==0.21.0
pip install pyttsx3==2.90
pip install pillow==10.0.0
pip install h5py==3.9.0

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the iris recognition system:
echo 1. Open command prompt in this folder
echo 2. Run: iris_env\Scripts\activate.bat
echo 3. Run: python Main.py
echo.
echo Or simply run: run_iris_recognition.bat
echo.
pause
