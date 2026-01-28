@echo off
color 0A
echo ==============================================
echo    BIOMETRIC VOTING SYSTEM - GITHUB UPLOADER
echo ==============================================
echo.
echo PREPARATION CHECK:
echo 1. Your code is already cleaned and committed locally.
echo 2. Sensitive files (passwords/databases) are excluded for safety.
echo.
echo INSTRUCTIONS:
echo 1. Go to https://github.com/new
echo 2. Create a new repository (name it biometric-voting)
echo 3. Copy the URL (e.g. https://github.com/username/repo.git)
echo.
set /p REPO_URL="Paste your GitHub Repository URL here: "

if "%REPO_URL%"=="" (
    echo Error: URL cannot be empty.
    pause
    exit /b
)

echo.
echo [1/2] Linking to GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo [2/2] Pushing files to GitHub...
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ==============================================
    echo    SUCCESS! PROJECT UPLOADED COMPLETELY.
    echo ==============================================
) else (
    echo.
    echo Upload failed. Please check your URL or internet connection.
)
pause
