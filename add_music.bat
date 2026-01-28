@echo off
echo 🎵 Adding Background Music to Iris Recognition Video
echo =====================================================

echo 📦 Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg not found
    echo.
    echo 📥 Please install FFmpeg first:
    echo    1. Visit: https://www.gyan.dev/ffmpeg/builds/
    echo    2. Download ffmpeg-release-essentials.zip
    echo    3. Extract and add to PATH
    echo    4. Restart command prompt
    echo.
    echo 💡 Alternative: Use online video editor at Kapwing.com
    pause
    exit /b 1
)

echo ✅ FFmpeg found!
echo 🎬 Combining video and audio...

ffmpeg -y -i iris_recognition_with_music.mp4 -i enhanced_background_music.wav -c:v copy -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 -shortest -movflags +faststart iris_recognition_final_with_music.mp4

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Video with music created!
    echo 📁 File: iris_recognition_final_with_music.mp4
    echo 🎬 Your professional video is ready!
) else (
    echo.
    echo ❌ Failed to combine video and audio
    echo 💡 Try using online video editor at Kapwing.com
)

echo.
pause
