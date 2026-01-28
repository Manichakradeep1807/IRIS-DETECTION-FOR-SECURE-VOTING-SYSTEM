@echo off
echo ==============================================
echo    FINAL GIT UPLOADER (BYPASS SIZE LIMIT)
echo ==============================================

echo [1/6] Securing heavy model files...
if not exist "dev_archive\model_backups" mkdir "dev_archive\model_backups"
move /Y "model\*.h5" "dev_archive\model_backups\" >nul 2>&1
move /Y "model\*.weights.h5" "dev_archive\model_backups\" >nul 2>&1

echo [2/6] Refreshing Git Ignore rules...
(
echo __pycache__/
echo *.pyc
echo *.db
echo dev_archive/
echo logs/
echo receipts/
echo captured_iris/
echo *.h5
echo *.weights.h5
echo .vscode/
echo voting_results_password.txt
) > .gitignore

echo [3/6] Resetting Git history...
rmdir /s /q .git

echo [4/6] Initializing clean repository...
git init
git add .
git commit -m "Complete Project Upload (Models excluded)"

echo [5/6] Linking to GitHub...
git branch -M main
git remote add origin https://github.com/Manichakradeep1807/IRIS-DETECTION-FOR-SECURE-VOTING-SYSTEM.git

echo [6/6] Pushing to GitHub...
git push -u -f origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS! Project is online.
    echo Large models are safely kept in 'dev_archive\model_backups' locally.
) else (
    echo.
    echo Failed.
)
pause
