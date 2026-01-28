@echo off
echo 🎬 Iris Recognition Animation Video Creator
echo ==========================================

echo.
echo 📦 Installing required packages...
pip install opencv-python numpy

echo.
echo 🎬 Creating animation video...
python run_animation.py

echo.
echo ✨ Done! Check for iris_recognition_demo.mp4
pause
